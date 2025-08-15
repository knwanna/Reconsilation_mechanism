import { useState } from "react"
import { Box, CssBaseline, ThemeProvider, createTheme } from "@mui/material"
import QueryPanel from "./components/QueryPanel"
import ResultsView from "./components/ResultsView"
import Header from "./components/Header"
import { motion } from "framer-motion"
import "./assets/styles/main.scss"

const theme = createTheme({
  palette: {
    primary: { main: "#4a148c" },
    secondary: { main: "#ff6f00" }
  },
  typography: {
    fontFamily: '"Inter", sans-serif'
  }
})

export default function App() {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ 
        minHeight: "100vh",
        background: "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
      }}>
        <Header />
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <QueryPanel onSearch={setResults} setLoading={setLoading} />
          <ResultsView results={results} loading={loading} />
        </motion.div>
      </Box>
    </ThemeProvider>
  )
}
