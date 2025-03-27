import { useState } from 'react'
import './App.css'
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { SearchResults } from './components/ui/searchResults'
import { Separator } from '@radix-ui/react-separator'

interface SolrDocument {
  [key: string]: any;
}

interface SolrResponse {
  response: {
    docs: SolrDocument[];
  };
}

function App() {
  const [query, setQuery] = useState<string>(""); 
  const [results, setResults] = useState<Result[]>([]);
  const [error, setError] = useState<string | null>(null); // State to handle errors


  const getResults = async (event: React.ChangeEvent<HTMLInputElement>)=> {
    event.preventDefault();

    setQuery(event.target.value)
    const query_string = event.target.value

    try {
      const response = await fetch('http://localhost:5000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Specify JSON content type
        },
        body: JSON.stringify({query: query_string}) // Send as JSON object
      });
      console.log(response)
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      
      const data: SolrResponse = await response.json();
      setResults(data.response.docs || []); // Update results state with the docs array
      console.log(data.response.docs)
      setError(null); // Clear any previous errors
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred");
      }
    }
  }

  return (
    <div className='items-start'>
      <h1 className='text-9xl'>Cyber Attack News</h1>
      <form className='m-8 w-110'>
        <Input value={query} onChange={(e) => getResults(e)}/>
      </form>
      <Separator className="my-4"/>
      <div className="results">
        {!error && results.length > 0 ? (
          <SearchResults results={results} />
        ) : (
          <p>No Result Found</p>
        )}
      </div>
    </div>
  )
}

export default App
