import React, { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const Readme = () => {
  const [markdown, setMarkdown] = useState("");

  useEffect(() => {
    const GITHUB_README_URL =
      "https://raw.githubusercontent.com/JaimeRamosT/proyectoCG/refs/heads/main/README.md";

    fetch(GITHUB_README_URL)
      .then((response) => {
        if (!response.ok) {
          throw new Error("No se pudo cargar el README");
        }
        return response.text();
      })
      .then((text) => setMarkdown(text))
      .catch((error) => console.error(error));
  }, []);

  return (
    <div className="prose lg:prose-xl mx-auto mb-10 mt-24 px-4 text-gray-200">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ node, ...props }) => (
            <h1 className="text-white text-3xl font-bold mb-4" {...props} />
          ),
          h2: ({ node, ...props }) => (
            <h2 className="text-gray-100 text-2xl font-semibold mb-3" {...props} />
          ),
          h3: ({ node, ...props }) => (
            <h3 className="text-gray-100 text-xl font-medium mb-2" {...props} />
          ),
          p: ({ node, ...props }) => (
            <p className="text-gray-200 leading-7" {...props} />
          ),
          li: ({ node, ...props }) => (
            <li className="text-gray-200 leading-6" {...props} />
          ),
          a: ({ node, ...props }) => (
            <a className=" text-blue-700" {...props} />
          ),
          code: ({ node, ...props }) => (
            <code className="text-white" {...props} />
          ),
        }}
      >
        {markdown}
      </ReactMarkdown>
    </div>
  );
};

export default Readme;