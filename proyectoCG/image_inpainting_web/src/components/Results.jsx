// Results.jsx
import React, { useState, useEffect } from 'react'

const Results = ({ outputImageBase64 }) => {
  const RESULT_WIDTH = 600;
  const RESULT_HEIGHT = 500;
  const [imageDimensions, setImageDimensions] = useState({ width: 0, height: 0 });
  const [scale, setScale] = useState(1);

  useEffect(() => {
    if (outputImageBase64) {
      const img = new Image();
      img.src = `data:image/png;base64,${outputImageBase64}`;
      img.onload = () => {
        const aspectRatio = img.width / img.height;
        let newWidth = RESULT_WIDTH;
        let newHeight = RESULT_HEIGHT;
  
        if (aspectRatio > RESULT_WIDTH / RESULT_HEIGHT) {
          newWidth = RESULT_WIDTH;
          newHeight = RESULT_WIDTH / aspectRatio;
          setScale(img.width / RESULT_WIDTH);
        } else {
          newHeight = RESULT_HEIGHT;
          newWidth = RESULT_HEIGHT * aspectRatio;
          setScale(img.height / RESULT_HEIGHT);
        }
  
        setImageDimensions({ width: newWidth, height: newHeight });
      };
    }
  }, [outputImageBase64]);

  return (
    <div className="flex flex-col items-center min-h-[40rem] w-1/2">
      <h2 className="text-xl font-bold text-white mb-4">
        Resultado del procesamiento
      </h2>
      <div
        className="border border-gray-300 shadow-lg rounded-md overflow-hidden flex items-center justify-center bg-gray-700"
        style={{ 
          width: `${RESULT_WIDTH}px`, 
          height: `${RESULT_HEIGHT}px`,
        }}
      >
        {outputImageBase64 ? (
          <div 
            className="w-full h-full flex items-center justify-center"
            style={{
              width: `${RESULT_WIDTH}px`,
              height: `${RESULT_HEIGHT}px`,
            }}
          >
            <img
              style={{
                width: `${imageDimensions.width}px`,
                height: `${imageDimensions.height}px`,
                imageRendering: 'high-quality',
                transform: 'translateZ(0)',
                position: 'absolute',
                objectFit: 'contain',
                pixelRatio: 2,
                imageSmoothingEnabled: false,
                quality: 1
              }}
              src={`data:image/png;base64,${outputImageBase64}`}
              alt="Result of image inpainting"
            />
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center">
            <svg
              className="w-16 h-16 mb-4 text-gray-500 dark:text-gray-400"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 20 16"
            >
              <path
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
              />
            </svg>
            <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
              Here will appear your results!
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Results;