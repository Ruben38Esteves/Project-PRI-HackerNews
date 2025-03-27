import React from "react";
import SearchResult from "./searchResult";

interface Result {
  author: string;
  title: string;
  url: string;
  date: string;
}

interface SearchResultsProps {
  results: Result[];
}

const SearchResults: React.FC<SearchResultsProps> = ({ results }) => {
  return (
    <div className="search-results">
      {results.length === 0 ? (
        <p>No results found.</p>
      ) : (
        results.map((result, index) => (
          <SearchResult
            key={index}
            author={result.author}
            title={result.title}
            url={result.url}
            date={result.date}
          />
        ))
      )}
    </div>
  );
};

export { SearchResults };
