"use client";
import { useEffect, useRef, useState } from "react";
import { motion, useAnimation } from "framer-motion";

export const TextGenerateEffect = ({
  words,
  className,
  filter = true,
  duration = 0.2,
}: {
  words: string;
  className?: string;
  filter?: boolean;
  duration?: number;
}) => {
  const [scope, setScope] = useState<string[]>([]);
  const controls = useAnimation();
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const wordsArray = words.split(" ");
    setScope(wordsArray);
  }, [words]);

  const animateWords = async () => {
    if (!containerRef.current) return;
    
    const wordElements = containerRef.current.querySelectorAll(".word");
    for (let i = 0; i < wordElements.length; i++) {
      await controls.start({
        opacity: 1,
        filter: filter ? "blur(0px)" : "none",
        transition: { duration: duration },
      });
      // Добавим небольшую задержку между анимациями слов
      await new Promise(resolve => setTimeout(resolve, duration * 1000));
    }
  };

  useEffect(() => {
    if (scope.length > 0) {
      animateWords();
    }
  }, [scope]);

  return (
    <div className={className}>
      <div ref={containerRef}>
        {scope.map((word, idx) => (
          <motion.span
            key={word + idx}
            className="word inline-block opacity-0"
            style={{
              filter: filter ? "blur(10px)" : "none",
            }}
            animate={controls}
          >
            {word}{" "}
          </motion.span>
        ))}
      </div>
    </div>
  );
};