import React, { useRef, useState, useEffect } from "react";
import { Stage, Layer, Line, Image as KonvaImage } from "react-konva";

function Canvas({ image, handleRemoveImage, handleOutputImage }) {
  // Definimos tamaño fijo del canvas
  const CANVAS_WIDTH = 600;
  const CANVAS_HEIGHT = 500;

  // Añadimos estado para el factor de escala
  const [scale, setScale] = useState(1);

  const [originalDimensions, setOriginalDimensions] = useState({ width: 0, height: 0 });

  const [isDrawing, setIsDrawing] = useState(false);
  const [lines, setLines] = useState([]);
  const [imageDimensions, setImageDimensions] = useState({ width: CANVAS_WIDTH, height: CANVAS_HEIGHT });
  const [konvaImage, setKonvaImage] = useState(null);
  const stageRef = useRef(null);
  const maskCanvasRef = useRef(null);

  // Modificar useEffect
  useEffect(() => {
    const img = new window.Image();
    img.src = image;
    img.onload = () => {
      setOriginalDimensions({ width: img.width, height: img.height });
      
      const aspectRatio = img.width / img.height;
      let newWidth = CANVAS_WIDTH;
      let newHeight = CANVAS_HEIGHT;
  
      if (aspectRatio > CANVAS_WIDTH / CANVAS_HEIGHT) {
        newWidth = CANVAS_WIDTH;
        newHeight = CANVAS_WIDTH / aspectRatio;
        setScale(img.width / CANVAS_WIDTH);
      } else {
        newHeight = CANVAS_HEIGHT;
        newWidth = CANVAS_HEIGHT * aspectRatio;
        setScale(img.height / CANVAS_HEIGHT);
      }
  
      setImageDimensions({ width: newWidth, height: newHeight });
      setKonvaImage(img);
    };
  }, [image]);

  // Función para verificar si un punto está dentro de la imagen
  const isPointInImage = (x, y) => {
    const imageX = (CANVAS_WIDTH - imageDimensions.width) / 2;
    const imageY = (CANVAS_HEIGHT - imageDimensions.height) / 2;
    
    return (
      x >= imageX &&
      x <= imageX + imageDimensions.width &&
      y >= imageY &&
      y <= imageY + imageDimensions.height
    );
  };

  
  // Modificar handleMouseDown
  const handleMouseDown = () => {
    const pos = stageRef.current.getPointerPosition();
    if (isPointInImage(pos.x, pos.y)) {
      setIsDrawing(true);
      setLines([...lines, { points: [pos.x, pos.y] }]);
    }
  };

  // Modificar handleMouseMove
  const handleMouseMove = () => {
    if (!isDrawing) return;

    const point = stageRef.current.getPointerPosition();
    if (isPointInImage(point.x, point.y)) {
      const lastLine = lines[lines.length - 1];
      lastLine.points = lastLine.points.concat([point.x, point.y]);
      setLines(lines.slice(0, -1).concat(lastLine));
    } else {
      // Detener el dibujo si el mouse sale de la imagen
      setIsDrawing(false);
    }
  };

  const handleMouseUp = () => {
    setIsDrawing(false);
  };

  // Modificar handleSaveMask
  // Modificar handleSaveMask para escalar las líneas correctamente
const handleSaveMask = () => {
  const maskCanvas = maskCanvasRef.current;
  const maskContext = maskCanvas.getContext("2d");
  
  // Usamos las dimensiones del canvas en vez de las originales
  maskCanvas.width = CANVAS_WIDTH;
  maskCanvas.height = CANVAS_HEIGHT;

  // Fondo blanco
  maskContext.fillStyle = "white";
  maskContext.fillRect(0, 0, maskCanvas.width, maskCanvas.height);
  
  // Dibujar líneas en negro
  maskContext.strokeStyle = "black";
  maskContext.lineWidth = 10;
  maskContext.lineJoin = "round";
  maskContext.lineCap = "round";

  // Dibujamos las líneas exactamente como se ven en el canvas
  lines.forEach((line) => {
    maskContext.beginPath();
    maskContext.moveTo(line.points[0], line.points[1]);
    for (let i = 2; i < line.points.length; i += 2) {
      maskContext.lineTo(line.points[i], line.points[i + 1]);
    }
    maskContext.stroke();
  });

  maskCanvas.toBlob(async (maskBlob) => {
    try {
      // Redimensionar la imagen original al tamaño del canvas
      const img = new Image();
      img.src = image;
      const resizedCanvas = document.createElement('canvas');
      resizedCanvas.width = CANVAS_WIDTH;
      resizedCanvas.height = CANVAS_HEIGHT;
      const ctx = resizedCanvas.getContext('2d');
      
      // Esperar a que la imagen cargue
      await new Promise((resolve) => {
        img.onload = resolve;
      });

      // Dibujar imagen redimensionada
      ctx.drawImage(img, 
        (CANVAS_WIDTH - imageDimensions.width) / 2, 
        (CANVAS_HEIGHT - imageDimensions.height) / 2,
        imageDimensions.width,
        imageDimensions.height
      );

      const resizedBlob = await new Promise(resolve => resizedCanvas.toBlob(resolve, 'image/jpeg', 1.0));

      // Enviar al servidor
      const formData = new FormData();
      formData.append("original_image", resizedBlob, "original_image.jpg");
      formData.append("mask", maskBlob, "mask.png");

      const response = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

      const result = await response.json();
      handleOutputImage(result.output_image.data);
    } catch (error) {
      console.error("Error al subir las imágenes:", error);
    }
  });
};

  return (
    <div className="flex flex-col items-center min-h-[40rem] w-1/2">
      <h2 className="text-xl font-bold text-white mb-4">
        Sombrea la parte que deseas rellenar
      </h2>

      {/* Contenedor con tamaño fijo */}
      <div className="border border-gray-300 shadow-lg rounded-md overflow-hidden"
           style={{ width: `${CANVAS_WIDTH}px`, height: `${CANVAS_HEIGHT}px` }}>
        <Stage
          ref={stageRef}
          width={CANVAS_WIDTH}
          height={CANVAS_HEIGHT}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          className="cursor-crosshair"
        >
          <Layer>
            {konvaImage && (
              // En el render del KonvaImage
              <KonvaImage
              image={konvaImage}
              width={imageDimensions.width}
              height={imageDimensions.height}
              x={(CANVAS_WIDTH - imageDimensions.width) / 2}
              y={(CANVAS_HEIGHT - imageDimensions.height) / 2}
              imageSmoothingEnabled={false}
              quality={1}
              pixelRatio={2} // Aumentar la densidad de píxeles
            />
            )}
          </Layer>
          <Layer>
            {/* Dibuja las líneas del usuario */}
            {lines.map((line, i) => (
              <Line
                points={line.points}
                stroke="rgba(255, 255, 255, 0.5)"
                strokeWidth={10 / scale} // Ajustar grosor según escala
                lineCap="round"
                lineJoin="round"
                globalCompositeOperation="source-over"
              />
            ))}
          </Layer>
        </Stage>
      </div>

      {/* Botón para guardar la máscara */}
      <div className="p-2 flex gap-5">
        <button
          onClick={handleSaveMask}
          className="mt-4 px-6 py-2 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700 transition"
        >
          Guardar Máscara
        </button>

        <button
          onClick={handleRemoveImage}
          className="mt-4 px-6 py-2 bg-red-600 text-white font-semibold rounded hover:bg-red-700 transition"
        >
          Quitar Imagen
        </button>
      </div>

      {/* Canvas oculto para generar la máscara */}
      <canvas
        ref={maskCanvasRef}
        width={imageDimensions.width}
        height={imageDimensions.height}
        style={{ display: "none" }}
      />
    </div>
  );
}

export default Canvas;