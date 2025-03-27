import React from "react";

interface SearchResultProps {
  author: string;
  title: string;
  url: string;
  date: string;
}

const SearchResult: React.FC<SearchResultProps> = ({ author, title, url, date }) => {
  return (
    <div className="p-2 m-10 rounded-lg border-2 border-black border-solid bg-gray-300 hover:scale-105 transition-transform duration-200">
      <a href={url} target="_blank" rel="noopener noreferrer" className="text-inherit no-underline text-black hover:text-black">
          <div className="">
              <h3 className="text-xl font-bold">{title}</h3>
              <p> {author}</p>
              <p>{date}</p>
          </div>
      </a>
    </div>
  );
};

export default SearchResult;
