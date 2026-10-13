#!/usr/bin/env python3
"""
Context Portal Database Manager
SQLite database operations for context portal
"""

import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

class ContextPortalDB:
    """SQLite database manager for Context Portal"""
    
    def __init__(self, db_path: str = "context.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Connect to database and create tables if not exists"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()
        return self
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def _create_tables(self):
        """Create database tables"""
        
        # Entities table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                domain TEXT NOT NULL,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                content_hash TEXT,
                token_count INTEGER,
                source_file TEXT,
                source_type TEXT,
                iteration_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Relations table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS relations (
                id TEXT PRIMARY KEY,
                from_entity TEXT NOT NULL,
                from_domain TEXT NOT NULL,
                to_entity TEXT NOT NULL,
                to_domain TEXT NOT NULL,
                relation_type TEXT NOT NULL,
                iteration_id TEXT,
                confidence REAL DEFAULT 1.0,
                is_cross_domain BOOLEAN,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (from_entity) REFERENCES entities(id),
                FOREIGN KEY (to_entity) REFERENCES entities(id)
            )
        """)
        
        # Versions table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS versions (
                iteration_id TEXT PRIMARY KEY,
                date DATE NOT NULL,
                summary TEXT,
                entity_count INTEGER,
                parent_iteration TEXT,
                snapshot_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_iteration) REFERENCES versions(iteration_id)
            )
        """)
        
        # Chunks table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id TEXT PRIMARY KEY,
                entity_id TEXT NOT NULL,
                content TEXT NOT NULL,
                chunk_type TEXT,
                start_line INTEGER,
                end_line INTEGER,
                token_count INTEGER,
                FOREIGN KEY (entity_id) REFERENCES entities(id)
            )
        """)
        
        # Create indexes
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_entities_domain ON entities(domain)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_entities_iteration ON entities(iteration_id)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_relations_from ON relations(from_entity)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_relations_to ON relations(to_entity)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_relations_type ON relations(relation_type)")
        
        self.conn.commit()
    
    def insert_entity(self, entity: Dict) -> str:
        """Insert or update an entity"""
        entity_id = entity['id']
        content_hash = hashlib.md5(entity['content'].encode()).hexdigest()
        
        # Check if exists
        self.cursor.execute("SELECT content_hash FROM entities WHERE id = ?", (entity_id,))
        existing = self.cursor.fetchone()
        
        if existing:
            # Update if content changed
            if existing['content_hash'] != content_hash:
                self.cursor.execute("""
                    UPDATE entities 
                    SET name = ?, domain = ?, type = ?, content = ?, 
                        content_hash = ?, token_count = ?, source_file = ?, 
                        source_type = ?, iteration_id = ?, updated_at = ?
                    WHERE id = ?
                """, (
                    entity['name'], entity['domain'], entity['type'],
                    entity['content'], content_hash, entity.get('token_count'),
                    entity.get('source_file'), entity.get('source_type'),
                    entity.get('iteration_id'), datetime.now(), entity_id
                ))
        else:
            # Insert new
            self.cursor.execute("""
                INSERT INTO entities (id, name, domain, type, content, content_hash, 
                                     token_count, source_file, source_type, iteration_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entity_id, entity['name'], entity['domain'], entity['type'],
                entity['content'], content_hash, entity.get('token_count'),
                entity.get('source_file'), entity.get('source_type'), entity.get('iteration_id')
            ))
        
        self.conn.commit()
        return entity_id
    
    def insert_relation(self, relation: Dict) -> str:
        """Insert a relation between entities"""
        relation_id = f"{relation['from_entity']}->{relation['to_entity']}:{relation['relation_type']}"
        
        self.cursor.execute("""
            INSERT OR REPLACE INTO relations 
            (id, from_entity, from_domain, to_entity, to_domain, relation_type, 
             iteration_id, confidence, is_cross_domain, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            relation_id, relation['from_entity'], relation['from_domain'],
            relation['to_entity'], relation['to_domain'], relation['relation_type'],
            relation.get('iteration_id'), relation.get('confidence', 1.0),
            relation.get('is_cross_domain', False),
            json.dumps(relation.get('metadata', {})) if relation.get('metadata') else None
        ))
        
        self.conn.commit()
        return relation_id
    
    def get_entity(self, entity_id: str) -> Optional[Dict]:
        """Get entity by ID"""
        self.cursor.execute("SELECT * FROM entities WHERE id = ?", (entity_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_entities_by_domain(self, domain: str, entity_type: Optional[str] = None) -> List[Dict]:
        """Get entities by domain and optional type"""
        if entity_type:
            self.cursor.execute(
                "SELECT * FROM entities WHERE domain = ? AND type = ?",
                (domain, entity_type)
            )
        else:
            self.cursor.execute(
                "SELECT * FROM entities WHERE domain = ?",
                (domain,)
            )
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_relations(self, entity_id: str, relation_type: Optional[str] = None) -> List[Dict]:
        """Get relations for an entity"""
        if relation_type:
            self.cursor.execute("""
                SELECT * FROM relations 
                WHERE (from_entity = ? OR to_entity = ?) AND relation_type = ?
            """, (entity_id, entity_id, relation_type))
        else:
            self.cursor.execute("""
                SELECT * FROM relations 
                WHERE from_entity = ? OR to_entity = ?
            """, (entity_id, entity_id))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_conflicts(self) -> List[Dict]:
        """Get all conflicting relations"""
        self.cursor.execute("SELECT * FROM relations WHERE relation_type = 'conflicts'")
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_orphan_rules(self) -> List[Dict]:
        """Get all orphan rules (code rules without product mapping)"""
        self.cursor.execute("""
            SELECT e.* FROM entities e
            WHERE e.domain = 'code' AND e.type = 'rule'
            AND e.id NOT IN (
                SELECT to_entity FROM relations WHERE relation_type = 'validates'
            )
        """)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def search_entities(self, keyword: str, domain: Optional[str] = None) -> List[Dict]:
        """Search entities by keyword"""
        query = "SELECT * FROM entities WHERE content LIKE ?"
        params = [f"%{keyword}%"]
        
        if domain:
            query += " AND domain = ?"
            params.append(domain)
        
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def record_version(self, iteration_id: str, summary: str, entity_count: int, 
                       parent_iteration: Optional[str] = None, snapshot_path: Optional[str] = None):
        """Record a version snapshot"""
        self.cursor.execute("""
            INSERT OR REPLACE INTO versions 
            (iteration_id, date, summary, entity_count, parent_iteration, snapshot_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            iteration_id, datetime.now().date(), summary, entity_count,
            parent_iteration, snapshot_path
        ))
        self.conn.commit()
    
    def get_version_history(self) -> List[Dict]:
        """Get version history"""
        self.cursor.execute("SELECT * FROM versions ORDER BY date")
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        stats = {}
        
        # Entity counts by domain and type
        self.cursor.execute("""
            SELECT domain, type, COUNT(*) as count 
            FROM entities 
            GROUP BY domain, type
        """)
        stats['entity_counts'] = [dict(row) for row in self.cursor.fetchall()]
        
        # Total entities
        self.cursor.execute("SELECT COUNT(*) FROM entities")
        stats['total_entities'] = self.cursor.fetchone()[0]
        
        # Total relations
        self.cursor.execute("SELECT COUNT(*) FROM relations")
        stats['total_relations'] = self.cursor.fetchone()[0]
        
        # Conflicts count
        self.cursor.execute("SELECT COUNT(*) FROM relations WHERE relation_type = 'conflicts'")
        stats['conflicts_count'] = self.cursor.fetchone()[0]
        
        # Orphan rules count
        self.cursor.execute("""
            SELECT COUNT(*) FROM entities e
            WHERE e.domain = 'code' AND e.type = 'rule'
            AND e.id NOT IN (
                SELECT to_entity FROM relations WHERE relation_type = 'validates'
            )
        """)
        stats['orphan_rules_count'] = self.cursor.fetchone()[0]
        
        return stats


def main():
    """CLI for database operations"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Context Portal Database Manager')
    parser.add_argument('--db', default='context.db', help='Database path')
    parser.add_argument('--init', action='store_true', help='Initialize database')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--search', help='Search keyword')
    parser.add_argument('--domain', help='Filter by domain')
    parser.add_argument('--conflicts', action='store_true', help='Show conflicts')
    parser.add_argument('--orphans', action='store_true', help='Show orphan rules')
    
    args = parser.parse_args()
    
    db = ContextPortalDB(args.db).connect()
    
    try:
        if args.init:
            print(f"Database initialized: {args.db}")
        
        elif args.stats:
            stats = db.get_statistics()
            print("\n=== Database Statistics ===")
            print(f"Total Entities: {stats['total_entities']}")
            print(f"Total Relations: {stats['total_relations']}")
            print(f"Conflicts: {stats['conflicts_count']}")
            print(f"Orphan Rules: {stats['orphan_rules_count']}")
            print("\nEntity Counts by Domain/Type:")
            for item in stats['entity_counts']:
                print(f"  {item['domain']}/{item['type']}: {item['count']}")
        
        elif args.search:
            results = db.search_entities(args.search, args.domain)
            print(f"\n=== Search Results for '{args.search}' ===")
            for entity in results:
                print(f"[{entity['domain']}/{entity['type']}] {entity['name']}")
                print(f"  ID: {entity['id']}")
                print(f"  Source: {entity.get('source_file', 'N/A')}")
                print()
        
        elif args.conflicts:
            conflicts = db.get_conflicts()
            print(f"\n=== Conflicts ({len(conflicts)}) ===")
            for rel in conflicts:
                from_entity = db.get_entity(rel['from_entity'])
                to_entity = db.get_entity(rel['to_entity'])
                print(f"\n{from_entity['name']} -> {to_entity['name']}")
                print(f"  Type: {rel['relation_type']}")
                print(f"  Confidence: {rel['confidence']}")
        
        elif args.orphans:
            orphans = db.get_orphan_rules()
            print(f"\n=== Orphan Rules ({len(orphans)}) ===")
            for entity in orphans:
                print(f"\n{entity['name']}")
                print(f"  ID: {entity['id']}")
                print(f"  Source: {entity.get('source_file', 'N/A')}")
                print(f"  Content: {entity['content'][:100]}...")
        
        else:
            parser.print_help()
    
    finally:
        db.close()


if __name__ == '__main__':
    main()
