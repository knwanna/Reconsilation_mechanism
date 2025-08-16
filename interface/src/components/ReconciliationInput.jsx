import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Chip, Box } from '@mui/material';
import { CheckCircle, XCircle, AlertTriangle } from 'lucide-react';

export default function ResultsVisualizer({ results }) {
  if (!results || results.length === 0) {
    return (
      <Box sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="body1" color="textSecondary">
          No reconciliation results to display
        </Typography>
      </Box>
    );
  }

  return (
    <TableContainer component={Paper} sx={{ mt: 4, maxHeight: 600 }}>
      <Table stickyHeader aria-label="reconciliation results">
        <TableHead>
          <TableRow>
            <TableCell>Source Value</TableCell>
            <TableCell>Matched Value</TableCell>
            <TableCell>Confidence</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {results.map((row, index) => (
            <TableRow key={index}>
              <TableCell sx={{ fontFamily: 'monospace' }}>{row.source}</TableCell>
              <TableCell sx={{ fontFamily: 'monospace' }}>
                {row.match || <Typography color="error">No match found</Typography>}
              </TableCell>
              <TableCell>
                {row.confidence ? (
                  <Chip 
                    label={`${(row.confidence * 100).toFixed(1)}%`}
                    color={
                      row.confidence > 0.9 ? 'success' : 
                      row.confidence > 0.7 ? 'warning' : 'error'
                    }
                    size="small"
                  />
                ) : 'N/A'}
              </TableCell>
              <TableCell>
                {row.status === 'matched' ? (
                  <Chip 
                    icon={<CheckCircle size={16} />}
                    label="Matched"
                    color="success"
                    size="small"
                  />
                ) : row.status === 'partial' ? (
                  <Chip
                    icon={<AlertTriangle size={16} />}
                    label="Partial"
                    color="warning"
                    size="small"
                  />
                ) : (
                  <Chip
                    icon={<XCircle size={16} />}
                    label="Unmatched"
                    color="error"
                    size="small"
                  />
                )}
              </TableCell>
              <TableCell>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Chip 
                    label="View Details" 
                    variant="outlined" 
                    size="small"
                    clickable
                  />
                  {row.status !== 'matched' && (
                    <Chip
                      label="Manual Match"
                      color="primary"
                      size="small"
                      clickable
                    />
                  )}
                </Box>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}