import { Table, TableBody, TableCell, TableRow } from '@mui/material';

export default function CSVTable({ data }) {
  return (
    <Table>
      <TableBody>
        {data.map((row, i) => (
          <TableRow key={i}>
            {row.map((cell, j) => (
              <TableCell key={j}>{cell}</TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}