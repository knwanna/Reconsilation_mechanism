import { TextField, Button } from '@mui/material';

export default function ReconciliationInput() {
  return (
    <div className="input-section">
      <TextField 
        multiline 
        rows={4} 
        fullWidth
        label="Enter data to reconcile"
      />
      <Button variant="contained" sx={{ mt: 2 }}>
        Process
      </Button>
    </div>
  );
}