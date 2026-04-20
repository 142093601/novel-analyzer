#!/usr/bin/env python3
"""
Novel text chunker - splits long novel text into manageable chunks for analysis.
Usage: python3 chunk_novel.py <input_file> [--words-per-chunk 3000] [--output-dir ./chunks]
"""

import sys
import os
import argparse
import re


def split_by_chapter(text):
    """Split text by common chapter markers."""
    # Common chapter patterns: 第X章, Chapter X, 卷X, 第X节, or standalone numbers
    chapter_pattern = re.compile(
        r'\n\s*(第[一二三四五六七八九十百千\d]+[章节卷回篇]|'
        r'Chapter\s+\d+|'
        r'卷[一二三四五六七八九十\d]+|'
        r'CHAPTER\s+\d+|'
        r'序[章幕]|'
        r'尾[声声]|'
        r'番外)\s*\n',
        re.IGNORECASE
    )
    
    splits = chapter_pattern.split(text)
    if len(splits) <= 1:
        return None  # No chapter markers found
    
    chunks = []
    for i in range(0, len(splits) - 1, 2):
        header = splits[i + 1] if i + 1 < len(splits) else ""
        content = splits[i] if i > 0 else ""
        if i + 2 < len(splits):
            content = splits[i + 2]
        chunks.append((header.strip(), content.strip()))
    
    # Rebuild properly
    parts = chapter_pattern.split(text)
    result = []
    for i, part in enumerate(parts):
        part = part.strip()
        if part and len(part) > 50:  # Skip very short fragments
            result.append(part)
    
    return result if len(result) > 1 else None


def split_by_words(text, words_per_chunk=3000):
    """Split text into chunks of approximately N words (Chinese: characters)."""
    # Detect if Chinese
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(text)
    is_chinese = chinese_chars / max(total_chars, 1) > 0.3
    
    if is_chinese:
        # For Chinese, split by characters
        chunk_size = words_per_chunk * 2  # Chinese chars roughly = words
        paragraphs = text.split('\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = para + "\n"
            else:
                current_chunk += para + "\n"
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
    else:
        # For English, split by word count
        words = text.split()
        chunks = []
        for i in range(0, len(words), words_per_chunk):
            chunk = ' '.join(words[i:i + words_per_chunk])
            chunks.append(chunk)
    
    return chunks


def main():
    parser = argparse.ArgumentParser(description='Split novel text into analysis chunks')
    parser.add_argument('input_file', help='Path to the novel text file')
    parser.add_argument('--words-per-chunk', type=int, default=3000,
                        help='Approximate words per chunk (default: 3000)')
    parser.add_argument('--output-dir', default='./chunks',
                        help='Output directory for chunks (default: ./chunks)')
    parser.add_argument('--method', choices=['chapter', 'words', 'auto'], default='auto',
                        help='Split method (default: auto)')
    
    args = parser.parse_args()
    
    with open(args.input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"Input: {args.input_file}")
    print(f"Total length: {len(text)} characters")
    
    # Determine split method
    if args.method == 'auto':
        chunks_by_chapter = split_by_chapter(text)
        if chunks_by_chapter and len(chunks_by_chapter) > 1:
            chunks = chunks_by_chapter
            method = 'chapter'
        else:
            chunks = split_by_words(text, args.words_per_chunk)
            method = 'words'
    elif args.method == 'chapter':
        chunks = split_by_chapter(text)
        if not chunks:
            print("No chapter markers found, falling back to word-based split")
            chunks = split_by_words(text, args.words_per_chunk)
            method = 'words'
        else:
            method = 'chapter'
    else:
        chunks = split_by_words(text, args.words_per_chunk)
        method = 'words'
    
    print(f"Split method: {method}")
    print(f"Total chunks: {len(chunks)}")
    
    # Write chunks
    os.makedirs(args.output_dir, exist_ok=True)
    for i, chunk in enumerate(chunks, 1):
        chunk_file = os.path.join(args.output_dir, f"chunk_{i:03d}.txt")
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(chunk)
        print(f"  Chunk {i}: {len(chunk)} chars → {chunk_file}")
    
    # Write manifest
    manifest_file = os.path.join(args.output_dir, 'manifest.json')
    import json
    manifest = {
        'source': args.input_file,
        'method': method,
        'total_chunks': len(chunks),
        'total_chars': len(text),
        'chunks': [
            {
                'file': f'chunk_{i:03d}.txt',
                'chars': len(chunk),
                'preview': chunk[:100] + '...' if len(chunk) > 100 else chunk
            }
            for i, chunk in enumerate(chunks, 1)
        ]
    }
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"\nManifest: {manifest_file}")


if __name__ == '__main__':
    main()
