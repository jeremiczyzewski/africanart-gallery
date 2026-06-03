type Block = {
  type: string;
  text?: string;
  spans?: any[];
  direction?: string;
};

export default function RichText({ blocks, className = '' }: { blocks: Block[] | undefined; className?: string }) {
  if (!Array.isArray(blocks)) return null;
  return (
    <div className={className}>
      {blocks.map((b, i) => {
        const text = b.text || '';
        switch (b.type) {
          case 'heading1':
            return <h1 key={i} className="serif italic text-5xl md:text-6xl mb-6">{text}</h1>;
          case 'heading2':
            return <h2 key={i} className="serif italic text-3xl md:text-4xl mb-4 mt-8">{text}</h2>;
          case 'heading3':
            return <h3 key={i} className="serif italic text-2xl mb-3 mt-6">{text}</h3>;
          case 'heading4':
            return <h4 key={i} className="serif italic text-xl mb-2 mt-4">{text}</h4>;
          case 'preformatted':
            return <pre key={i} className="text-sm whitespace-pre-wrap mb-4">{text}</pre>;
          case 'paragraph':
          default:
            return (
              <p key={i} className="text-base leading-relaxed mb-4 whitespace-pre-line">
                {text}
              </p>
            );
        }
      })}
    </div>
  );
}
