import { useEffect, useRef, useState } from 'react';
import styles from './index.module.css';

const trees = [
  { color: 'red', path: './red/a.png' },
  { color: 'orange', path: './orange/a.png' },
  { color: 'blue', path: './blue/a.png' },
  { color: 'green', path: './green/a.png' },
  { color: 'black', path: './black/a.png' },
  { color: 'yellow', path: './yellow/a.png' },
  { color: 'purple', path: './purple/a.png' }
];

const EMOTION_COLOR_MAP = {
  "愤怒的": "red",
  "开心的": "yellow",
  "厌恶的": "green",
  "颓丧的": "black",
  "焦虑的": "purple",
  "恐惧的": "blue",
  "爱慕的": "orange"
};

const Tree = ({ color, imagePath, isActive }) => (
  <div className={`${styles.tree} ${isActive ? styles.active : ''}`}>
    <img
      src={imagePath}
      className={styles.treeFrame}
      alt={`${color} tree`}
      loading="lazy"
    />
  </div>
);

const TreeDisplay = () => {
  const [activeEmotion, setActiveEmotion] = useState(null);
  const [showInfo, setShowInfo] = useState(false);
  const [data, setData] = useState(null);
  const containerRef = useRef(null);
  const styleElements = useRef([]);
  const infoTimeout = useRef(null);

  const handleClick = () => {
    if (!activeEmotion || !data) return;

    setShowInfo(true);
    clearTimeout(infoTimeout.current);
    infoTimeout.current = setTimeout(() => {
      setShowInfo(false);
    }, 3000);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://192.168.110.78:8000/conditions/2025-03-02');
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const res = await response.json();
        if (res.records?.length > 0) {
          const validRecords = res.records.filter(record =>
            EMOTION_COLOR_MAP.hasOwnProperty(record.emotion)
          );

          if (validRecords.length > 0) {
            const targetRecord = validRecords[validRecords.length-1];
            setData(targetRecord.condition);
            setActiveEmotion(targetRecord.emotion);
          }
        }
      } catch (error) {
        console.error('请求失败:', error);
        setData('数据加载失败');
      }
    };
    fetchData();
  }, []);

  useEffect(() => {
    document.documentElement.style.overflow = 'hidden';
    document.body.style.overflow = 'hidden';

    const createSwayAnimation = (index) => {
      const animationName = `sway-${index}`;
      const styleEl = document.createElement('style');

      const getRandomTransform = () => ({
        scale: 1 + Math.random() * 0.03,
        rotate: (Math.random() * 1.5 - 0.75),
        skewX: (Math.random() * 0.5 - 0.25),
        skewY: (Math.random() * 0.5 - 0.25),
        translateX: (Math.random() * 4 - 2),
        translateY: (Math.random() * 4 - 2)
      });

      const keyframes = [0, 30, 60, 100].map(percent => {
        const t = getRandomTransform();
        return `
          ${percent}% {
            transform: 
              translate(${t.translateX}px, ${t.translateY}px)
              scale(${t.scale}) 
              rotate(${t.rotate}deg)
              skew(${t.skewX}deg, ${t.skewY}deg);
          }
        `;
      });

      styleEl.textContent = `
        @keyframes ${animationName} {
          ${keyframes.join('')}
        }
        .${styles.tree}:nth-child(${index + 1}) img {
          animation: ${animationName} ${15 + index * 2}s infinite ease-in-out;
        }
      `;

      document.head.appendChild(styleEl);
      styleElements.current.push(styleEl);
    };

    trees.forEach((_, index) => createSwayAnimation(index));

    return () => {
      styleElements.current.forEach(styleEl =>
        document.head.removeChild(styleEl)
      );
      document.documentElement.style.overflow = '';
      document.body.style.overflow = '';
      clearTimeout(infoTimeout.current);
    };
  }, []);

  return (
    <div
      className={styles.container}
      onClick={handleClick}
      style={{ cursor: (activeEmotion && data) ? 'pointer' : 'default' }}
    >
      {showInfo && activeEmotion && data && (
        <div className={styles.infoPanel}>
          <h3>{activeEmotion}</h3>
          <p>{data}</p>
        </div>
      )}

      <div ref={containerRef} className={styles.treeContainer}>
        {trees.map((tree) => {
          const targetColor = EMOTION_COLOR_MAP[activeEmotion] || '';
          return (
            <Tree
              key={tree.color}
              color={tree.color}
              imagePath={tree.path}
              isActive={targetColor === tree.color}
            />
          );
        })}
      </div>
    </div>
  );
};

export default TreeDisplay;