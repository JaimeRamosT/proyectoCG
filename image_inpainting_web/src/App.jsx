import { useState } from 'react'
import Canvas from './components/canvas'
import UploadImage from './components/UploadImage';
import Results from './components/Results';

function App() {
  const [image, setImage] = useState(null); // Imagen cargada por el usuario
  const [outputImage, setOutputImage] = useState(null); // Resultado del modelo

  const handleImageUpload = (file) => {
    const url = URL.createObjectURL(file);
    setImage(url); // Guarda la URL de la imagen
  };

  return (
    <>
      <div className='min-h-screen w-full px-2 flex flex-col justify-center items-center bg-[#111827]'>
        <h1 className='text-4xl font-bold text-white'>Residual Dense Image Inpainting CNN</h1>
        <div className='min-h-[90vh] flex flex-col justify-center items-center w-full max-w-[80%] '>
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
                  setOutputImage(result);  // Guardamos solo el base64
                }}
              />
              <Results outputImageBase64={outputImage}></Results>
            </div>
          )}
        </div>
      </div>
    </>
  )
}

export default App
