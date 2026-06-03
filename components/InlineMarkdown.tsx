/**
 * Prosty inline parser markdown: **bold**, *italic*, zachowanie newlines.
 * Bez zewnetrznej zaleznosci — wystarczy dla naszego use case (opisy eksponatow).
 *
 * Obsluguje:
 *   **tekst**       -> <strong>tekst</strong>
 *   *tekst*         -> <em>tekst</em>
 *   newlines        -> <br> (via whitespace-pre-line w stylu rodzica)
 *
 * NIE obsluguje (i to OK — opisy nie potrzebuja):
 *   linki [..](..) , kod `..`, naglowki #, listy -
 */
import React from 'react';

type Token = { type: 'text' | 'bold' | 'italic'; content: string };

function tokenize(input: string): Token[] {
  const tokens: Token[] = [];
  let i = 0;
  while (i < input.length) {
    // **bold**
    if (input[i] === '*' && input[i + 1] === '*') {
      const end = input.indexOf('**', i + 2);
      if (end !== -1) {
        tokens.push({ type: 'bold', content: input.slice(i + 2, end) });
        i = end + 2;
        continue;
      }
    }
    // *italic*  (single *, ale nie zaraz po znaku slowa — zeby uniknac false positive)
    if (input[i] === '*' && input[i + 1] !== '*') {
      const end = input.indexOf('*', i + 1);
      if (end !== -1 && end > i + 1) {
        tokens.push({ type: 'italic', content: input.slice(i + 1, end) });
        i = end + 1;
        continue;
      }
    }
    // text — zbieraj do najblizszego *
    let next = input.indexOf('*', i);
    if (next === -1) next = input.length;
    tokens.push({ type: 'text', content: input.slice(i, next) });
    i = next;
  }
  return tokens;
}

export default function InlineMarkdown({ children, className }: { children: string; className?: string }) {
  const tokens = tokenize(children || '');
  return (
    <div className={className} style={{ whiteSpace: 'pre-line' }}>
      {tokens.map((t, idx) => {
        if (t.type === 'bold') return <strong key={idx}>{t.content}</strong>;
        if (t.type === 'italic') return <em key={idx}>{t.content}</em>;
        return <React.Fragment key={idx}>{t.content}</React.Fragment>;
      })}
    </div>
  );
}
