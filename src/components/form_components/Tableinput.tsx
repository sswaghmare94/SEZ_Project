import { useState } from "react";       //If store values are changing continuously then useState is used  

interface TableinputProps {
  onUpdateTableData: (data: any[]) => void;
}

const Tableinput = ({ onUpdateTableData }: TableinputProps) => {
  const numberOfRows = 14; // Define the number of rows you want
  const [tableData, setTableData] = useState<any[]>([]);

  const renderRows = () => {
    const rows = [];

    for (let i = 0; i < numberOfRows; i++) {
      const serialNumber = i + 1;
      rows.push(
        <tr key={i}>
          <td>{serialNumber}</td>
          <td>
            <input
              type="text"
              className="form-control"
              onChange={(e) => handleTableDataChange(i, "name", e.target.value)}
            />
          </td>
          <td>
            <input
              type="number"
              className="form-control"
              step="1"
              min="0"
              onChange={(e) =>
                handleTableDataChange(i, "duration", e.target.value)
              }
            />
          </td>
          <td>
            <input
              type="number"
              className="form-control"
              step="0.001"
              min="0"
              onChange={(e) => handleTableDataChange(i, "cost", e.target.value)}
            />
          </td>
          <td>
            <input
              type="text"
              className="form-control"
              onChange={(e) =>
                handleTableDataChange(i, "predecessors", e.target.value)
              }
            />
          </td>
          <td>
            <input
              type="number"
              name={`man_power_${i}`}
              placeholder="Man Power"
              className="form-control m-2"
              step="1"
              min="0"
              onChange={(e) =>
                handleTableDataChange(i, "man_power", e.target.value)
              }
            />
            <input
              type="number"
              name={`machines_${i}`}
              placeholder="Machines"
              className="form-control m-2"
              step="1"
              min="0"
              onChange={(e) =>
                handleTableDataChange(i, "machines", e.target.value)
              }
            />
            <input
              type="number"
              name={`material_${i}`}
              placeholder="Material"
              className="form-control m-2"
              step="1"
              min="0"
              onChange={(e) =>
                handleTableDataChange(i, "material", e.target.value)
              }
            />
          </td>
        </tr>
      );
    }
    return rows;
  };
  const handleTableDataChange = (
    index: number,
    field: string,
    value: string
  ) => {
    const updatedData = [...tableData];
    if (!updatedData[index]) {
      updatedData[index] = {}; // Create a new object for the row if it doesn't exist
    }

    if (field === "predecessors") {
      updatedData[index][field] = validatePredecessors(value);
    } else {
      updatedData[index][field] = value;
    }

    // updatedData[index][field] = value;
    setTableData(updatedData);
    onUpdateTableData(updatedData);
  };

  const validatePredecessors = (value: string) => {
    // Split the input string by commas to get an array of serial numbers
    const serialNumbers = value.split(",");

    // Remove any leading or trailing whitespaces from each serial number
    const trimmedSerialNumbers = serialNumbers.map((num) => num.trim());

    // Filter out any empty serial numbers
    const filteredSerialNumbers = trimmedSerialNumbers.filter(
      (num) => num !== ""
    );

    // Convert the serial numbers to integers
    const predecessorNumbers = filteredSerialNumbers.map((num) =>
      parseInt(num, 10)
    );

    // Limit the number of predecessors to a maximum of 5
    const limitedPredecessors = predecessorNumbers.slice(0, 5);

    return limitedPredecessors;
  };

  return (
    <div className="container">
      <table className="table table-striped table-bordered">
        <thead>
          <tr>
            <th>Sr No</th>
            <th>Activity</th>
            <th>Duration</th>
            <th>cost</th>
            <th>Predecessor</th>
            <th>Resource</th>
          </tr>
        </thead>
        <tbody>{renderRows()}</tbody>
      </table>
    </div>
  );
};

export default Tableinput;