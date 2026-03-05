'use client';

export default function HebrewText({
  children,
  className = '',
  as: Tag = 'span',
}: {
  children: React.ReactNode;
  className?: string;
  as?: 'span' | 'div' | 'p' | 'td';
}) {
  return (
    <Tag dir="rtl" className={`font-hebrew ${className}`}>
      {children}
    </Tag>
  );
}
