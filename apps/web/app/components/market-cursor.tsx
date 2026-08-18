"use client";

import { useEffect, useRef } from "react";

export function MarketCursor() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    let frame = 0;
    const move = (event: MouseEvent) => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        node.style.transform = `translate3d(${event.clientX}px, ${event.clientY}px, 0)`;
      });
    };
    window.addEventListener("mousemove", move, { passive: true });
    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("mousemove", move);
    };
  }, []);

  return <div ref={ref} className="market-cursor" aria-hidden="true"><span /></div>;
}
