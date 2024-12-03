import React from 'react'

const Results = ({ outputImageBase64 }) => {
  return (
    <div
      className={`flex items-center justify-center w-1/2`}
    >
      <div
        className={`
            flex flex-col items-center justify-center w-full min-h-[40rem] border-2 border-gray-300
            dark:border-gray-600 border-dashed rounded-lg bg-gray-50 dark:bg-gray-700 
            `}
      >
        <div className="flex flex-col items-center justify-center w-full min-h-[40rem] pt-5 pb-6">
          {outputImageBase64 ? (
            <img
              className="object-contain min-w-full"
              src={`data:image/png;base64,${outputImageBase64}`}
              alt="Result of image inpainting"
            />
          ) : (
            <>
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
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default Results;