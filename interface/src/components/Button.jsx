import { useState, useRef } from 'react';

const Button = ({ children, onClick, disabled, className }) => {
  const [isPressing, setIsPressing] = useState(false);
  const pressTimeout = useRef(null);

  const handlePointerDown = () => {
    setIsPressing(true);
    if (pressTimeout.current) clearTimeout(pressTimeout.current);
  };

  const handlePointerUp = () => {
    pressTimeout.current = setTimeout(() => setIsPressing(false), 200);
  };

  return (
    <button
      onPointerDown={handlePointerDown}
      onPointerUp={handlePointerUp}
      onPointerLeave={handlePointerUp}
      onClick={onClick}
      disabled={disabled}
      className={`py-3 px-6 rounded-xl font-bold transition-all duration-200 transform
        ${disabled ? 'bg-gray-700 text-gray-400 cursor-not-allowed' : 'bg-purple-600 hover:bg-purple-700 active:bg-purple-800 text-white hover:scale-105'}
        ${isPressing ? 'scale-95' : 'scale-100'}
        ${className || ''}`}
    >
      {children}
    </button>
  );
};

export default Button;