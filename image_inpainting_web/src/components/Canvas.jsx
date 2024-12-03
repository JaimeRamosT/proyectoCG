import React, { useRef, useState, useEffect } from "react";
import { Stage, Layer, Line, Image as KonvaImage } from "react-konva";

function Canvas({ image, handleRemoveImage, handleOutputImage }) {
  const [isDrawing, setIsDrawing] = useState(false);
  const [lines, setLines] = useState([]);
  const [imageDimensions, setImageDimensions] = useState({ width: 800, height: 600 });
  const [konvaImage, setKonvaImage] = useState(null);
  const stageRef = useRef(null);
  const maskCanvasRef = useRef(null);

  // Cargar la imagen original y ajustar dimensiones del canvas
  useEffect(() => {
    const img = new window.Image();
    img.src = image;
    img.onload = () => {
      setImageDimensions({ width: img.width, height: img.height });
      setKonvaImage(img);
    };
  }, [image]);

  const handleMouseDown = () => {
    setIsDrawing(true);
    const pos = stageRef.current.getPointerPosition();
    setLines([...lines, { points: [pos.x, pos.y] }]);
  };

  const handleMouseMove = () => {
    if (!isDrawing) return;

    const stage = stageRef.current;
    const point = stage.getPointerPosition();
    const lastLine = lines[lines.length - 1];
    lastLine.points = lastLine.points.concat([point.x, point.y]);
    setLines(lines.slice(0, -1).concat(lastLine));
  };

  const handleMouseUp = () => {
    setIsDrawing(false);
  };

  const handleSaveMask = () => {
    const maskCanvas = maskCanvasRef.current;
    const maskContext = maskCanvas.getContext("2d");

    // Configurar fondo blanco y áreas pintadas en negro
    maskContext.clearRect(0, 0, maskCanvas.width, maskCanvas.height);
    maskContext.fillStyle = "white"; // Fondo blanco
    maskContext.fillRect(0, 0, maskCanvas.width, maskCanvas.height);

    // Dibuja las líneas en negro
    maskContext.strokeStyle = "black"; // Áreas pintadas en negro
    maskContext.lineWidth = 10;
    maskContext.lineJoin = "round";
    maskContext.lineCap = "round";

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
        // URL de tu servidor FastAPI
        const url = "http://127.0.0.1:8000/upload/";

        // Crear un Blob para la imagen original (ejemplo, esto puede cambiar según cómo obtienes la imagen original)
        const originalImageBlob = await fetch(image).then(res => res.blob());

        // Crear un objeto FormData
        const formData = new FormData();
        formData.append("original_image", originalImageBlob, "original_image.jpg");
        formData.append("mask", maskBlob, "mask.png");

        // Realizar la petición POST
        const response = await fetch(url, {
          method: "POST",
          body: formData,
        });

        // Verificar la respuesta
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Leer la respuesta como JSON
        const result = await response.json();
        handleOutputImage(result.output_image.data);
        console.log("Respuesta del servidor:", result);
      } catch (error) {
        console.error("Error al subir las imágenes:", error);
      }
    });
  };

  return (
    <div className="flex flex-col items-center min-h-[40rem] w-1/2">
      {/* Título */}
      <h2 className="text-xl font-bold text-white mb-4">
        Sombrea la parte que deseas rellenar
      </h2>

      {/* Canvas principal */}
      <div
        className="border border-gray-300 shadow-lg rounded-md overflow-hidden"
        style={{ width: imageDimensions.width, height: imageDimensions.height }}
      >
        <Stage
          ref={stageRef}
          width={imageDimensions.width}
          height={imageDimensions.height}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          className="cursor-crosshair"
        >
          <Layer>
            {/* Renderiza la imagen original */}
            {konvaImage && (
              <KonvaImage
                image={konvaImage}
                width={imageDimensions.width}
                height={imageDimensions.height}
              />
            )}
          </Layer>
          <Layer>
            {/* Dibuja las líneas del usuario */}
            {lines.map((line, i) => (
              <Line
                key={i}
                points={line.points}
                stroke="rgba(255, 255, 255, 0.5)" // Semitransparente para previsualización
                strokeWidth={10}
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