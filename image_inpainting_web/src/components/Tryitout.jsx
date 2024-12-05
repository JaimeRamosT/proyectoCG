import React, { useState } from "react";
import Canvas from './Canvas'
import UploadImage from './UploadImage';
import Results from './Results';

const Tryitout = () => {
  const [image, setImage] = useState(null); // Imagen cargada por el usuario
  const [outputImage, setOutputImage] = useState(null); // Resultado del modelo
  
  const handleImageUpload = (file) => {
    const url = URL.createObjectURL(file);
    setImage(url); // Guarda la URL de la imagen
  };

  return (
    <>
      <h1 className='text-4xl font-bold text-white mt-10'>Residual Dense Image Inpainting CNN</h1>
      <div className='min-h-[80vh] flex flex-col justify-center items-center w-full max-w-[80%] '>
        {!image ? (
          <UploadImage onImageUpload={handleImageUpload} />
        ) : (
          <div className='flex gap-5 w-full h-full'>
            <Canvas
              image={image}
              handleRemoveImage={() => {
                setImage(null);
                setOutputImage(null);
              }}
              handleOutputImage={(result) => {
                setOutputImage(result);
              }}
            />
            <Results outputImageBase64={outputImage}></Results>
          </div>
        )}
      </div>
    </>
  );
};

export default Tryitout;