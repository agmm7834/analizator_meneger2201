#!/usr/bin/env python3
"""
Fayl Tizimi Analizatori va Menedjer
Murakkab va foydali Python script
"""

import os
import sys
import hashlib
import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import argparse


class FileSystemAnalyzer:
    """Fayl tizimini tahlil qiluvchi va boshqaruvchi klass"""
    
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.stats = defaultdict(int)
        self.duplicates = defaultdict(list)
        self.file_types = defaultdict(list)
        
    def calculate_file_hash(self, filepath, block_size=65536):
        """Fayl hash qiymatini hisoblash (dublikatlarni topish uchun)"""
        hasher = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(block_size):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except (PermissionError, OSError):
            return None
    
    def format_size(self, size_bytes):
        """Baytlarni o'qish oson formatga o'tkazish"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def analyze_directory(self, find_duplicates=False):
        """Katalogni to'liq tahlil qilish"""
        print(f"\n🔍 Tahlil boshlanmoqda: {self.root_path}")
        print("=" * 60)
        
        total_size = 0
        file_hashes = {}
        
        for item in self.root_path.rglob('*'):
            if item.is_file():
                try:
                    size = item.stat().st_size
                    total_size += size
                    self.stats['total_files'] += 1
                    
                    # Fayl turini aniqlash
                    extension = item.suffix.lower() or 'no_extension'
                    self.file_types[extension].append({
                        'path': str(item),
                        'size': size,
                        'modified': datetime.fromtimestamp(item.stat().st_mtime)
                    })
                    
                    # Dublikatlarni topish
                    if find_duplicates:
                        file_hash = self.calculate_file_hash(item)
                        if file_hash:
                            if file_hash in file_hashes:
                                self.duplicates[file_hash].append(str(item))
                            else:
                                file_hashes[file_hash] = str(item)
                                self.duplicates[file_hash].append(str(item))
                    
                except (PermissionError, OSError) as e:
                    self.stats['errors'] += 1
                    
            elif item.is_dir():
                self.stats['total_dirs'] += 1
        
        self.stats['total_size'] = total_size
        return self.generate_report()
    
    def generate_report(self):
        """Tahlil hisobotini yaratish"""
        report = {
            'summary': {
                'total_files': self.stats['total_files'],
                'total_directories': self.stats['total_dirs'],
                'total_size': self.format_size(self.stats['total_size']),
                'total_size_bytes': self.stats['total_size'],
                'errors': self.stats['errors']
            },
            'file_types': {},
            'duplicates': []
        }
        
        # Fayl turlari bo'yicha statistika
        for ext, files in self.file_types.items():
            total = sum(f['size'] for f in files)
            report['file_types'][ext] = {
                'count': len(files),
                'total_size': self.format_size(total),
                'percentage': (total / self.stats['total_size'] * 100) if self.stats['total_size'] > 0 else 0
            }
        
        # Dublikatlar
        for file_hash, files in self.duplicates.items():
            if len(files) > 1:
                report['duplicates'].append({
                    'hash': file_hash,
                    'files': files,
                    'count': len(files)
                })
        
        return report
    
    def print_report(self, report):
        """Hisobotni chiroyli formatda chop etish"""
        print("\n📊 UMUMIY STATISTIKA")
        print("=" * 60)
        print(f"Jami fayllar: {report['summary']['total_files']}")
        print(f"Jami kataloglar: {report['summary']['total_directories']}")
        print(f"Umumiy hajm: {report['summary']['total_size']}")
        print(f"Xatolar: {report['summary']['errors']}")
        
        print("\n📁 FAYL TURLARI BO'YICHA STATISTIKA")
        print("=" * 60)
        sorted_types = sorted(
            report['file_types'].items(), 
            key=lambda x: x[1]['count'], 
            reverse=True
        )[:10]  # Top 10
        
        for ext, data in sorted_types:
            print(f"{ext:20} | Soni: {data['count']:6} | Hajm: {data['total_size']:12} | {data['percentage']:.1f}%")
        
        if report['duplicates']:
            print(f"\n🔄 DUBLIKAT FAYLLAR ({len(report['duplicates'])} guruh)")
            print("=" * 60)
            for dup in report['duplicates'][:5]:  # Birinchi 5 ta
                print(f"\nGuruh ({dup['count']} fayl):")
                for file in dup['files']:
                    print(f"  • {file}")
    
    def clean_duplicates(self, keep_first=True):
        """Dublikat fayllarni o'chirish"""
        cleaned = 0
        saved_space = 0
        
        print("\n🧹 Dublikatlar tozalanmoqda...")
        
        for file_hash, files in self.duplicates.items():
            if len(files) > 1:
                files_to_delete = files[1:] if keep_first else files[:-1]
                
                for filepath in files_to_delete:
                    try:
                        size = os.path.getsize(filepath)
                        os.remove(filepath)
                        cleaned += 1
                        saved_space += size
                        print(f"✓ O'chirildi: {filepath}")
                    except Exception as e:
                        print(f"✗ Xato: {filepath} - {e}")
        
        print(f"\n✅ {cleaned} ta fayl o'chirildi")
        print(f"💾 {self.format_size(saved_space)} joy bo'shatildi")
    
    def find_large_files(self, top_n=10):
        """Eng katta fayllarni topish"""
        all_files = []
        
        for files in self.file_types.values():
            all_files.extend(files)
        
        sorted_files = sorted(all_files, key=lambda x: x['size'], reverse=True)[:top_n]
        
        print(f"\n📦 ENG KATTA {top_n} FAYL")
        print("=" * 60)
        
        for i, file in enumerate(sorted_files, 1):
            print(f"{i}. {self.format_size(file['size']):12} - {file['path']}")
    
    def export_report(self, filename='report.json'):
        """Hisobotni JSON faylga eksport qilish"""
        report = self.generate_report()
        
        output_path = self.root_path / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\n💾 Hisobot saqlandi: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Fayl Tizimi Analizatori va Menedjer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Misollar:
  python file_system_analyzer.py /path/to/directory --analyze
  python file_system_analyzer.py /path/to/directory --duplicates
  python file_system_analyzer.py /path/to/directory --large-files 20
  python file_system_analyzer.py /path/to/directory --clean-duplicates
        """
    )
    
    parser.add_argument('path', help='Tahlil qilinadigan katalog yo\'li')
    parser.add_argument('-a', '--analyze', action='store_true', help='To\'liq tahlil')
    parser.add_argument('-d', '--duplicates', action='store_true', help='Dublikatlarni topish')
    parser.add_argument('-l', '--large-files', type=int, metavar='N', help='Eng katta N ta faylni ko\'rsatish')
    parser.add_argument('-c', '--clean-duplicates', action='store_true', help='Dublikatlarni o\'chirish')
    parser.add_argument('-e', '--export', metavar='FILE', help='Hisobotni JSON ga eksport qilish')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"❌ Xato: '{args.path}' topilmadi!")
        sys.exit(1)
    
    analyzer = FileSystemAnalyzer(args.path)
    
    # Tahlil
    if args.analyze or args.duplicates:
        report = analyzer.analyze_directory(find_duplicates=args.duplicates)
        analyzer.print_report(report)
    
    # Eng katta fayllar
    if args.large_files:
        if not args.analyze:
            analyzer.analyze_directory()
        analyzer.find_large_files(args.large_files)
    
    # Dublikatlarni tozalash
    if args.clean_duplicates:
        if not args.duplicates:
            print("⚠️  Avval --duplicates bilan tahlil qiling!")
            sys.exit(1)
        
        confirm = input("\n⚠️  Dublikatlarni o'chirishni tasdiqlaysizmi? (yes/no): ")
        if confirm.lower() in ['yes', 'y', 'ha']:
            analyzer.clean_duplicates()
        else:
            print("Bekor qilindi.")
    
    # Eksport
    if args.export:
        if not args.analyze:
            analyzer.analyze_directory(find_duplicates=args.duplicates)
        analyzer.export_report(args.export)


if __name__ == '__main__':
    main()
