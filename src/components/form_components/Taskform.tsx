import { useState } from "react";                //variable defined and stored in value and to change value of variables 
import Tableinput from "./Tableinput";           //component defined table input 
import { storeTaskData, getTaskData } from "../localStorage/localStorageUtils";  //function defined for storage and get data 
import { v4 as uuidv4 } from "uuid";             // uuid is to create unique id 

const Taskform = () => {
  const [projectname, setProjectName] = useState("");   //updating function in inital value
  const [planduration, setPlanDuration] = useState("");
  const [actualduration, setActualDuration] = useState("");
  const [tableData, setTableData] = useState<any[]>([]);
  const [imageContent, setImageContent] = useState("");
  const [messageContent, setMessageContent] = useState("");

  const handleSubmit = (e: any) => {           //function is created to fetch data from table inputs and stored variable in local storage
    e.preventDefault();                        // to stop refreshing everytime this function is defined 

    const activities = tableData.map((data) => ({      //map is one kind of for loop to iterate the data 
      name: data.name,    
      duration: parseFloat(data.duration || 0),     //parse float = null values are assigned zeros
      cost: parseFloat(data.cost || 0),
      predecessors: data.predecessors || [],
      resource_requirements: [
        parseFloat(data.man_power || 0),
        parseFloat(data.machines || 0),
        parseFloat(data.material || 0),
      ],
    }));

    const requestData = {
      project_name: projectname,
      project_duration: planduration,
      project_actual_duration: actualduration,
      activities: activities,
      userId: uuidv4(),        //to iterate the previous data need unique ID 
    };

    console.log("jsondata " + JSON.stringify(requestData));   //to print in browser : console.log

    fetch("http://127.0.0.1:5000/sez", {        //this link is API Key where data stored and fetch from this link
      method: "POST",                           // POST : after submitting value and stored in database (http methods : get post put delete)
      headers: {
        "Content-Type": "application/json",     //data stored in json format (easy method and widely used)
      },
      body: JSON.stringify(requestData),       //just to convert into string
    })
      .then((response) => response.json())      
      .then((data) => {
        // console.log(data.response);
        setImageContent(data.response);
        console.log("mydata " + data.response);
        setMessageContent(data.message);
        console.log("message " + data.message);
      })
      .then((error) => console.log(error));

    console.log("The project name is ", projectname);
    console.log("The plan duration is ", planduration);
    console.log("The actual duration is ", actualduration);
    console.log("The table data is ", tableData);

    // Create a new task object with the form field values
    // const newTask = {
    //   name: projectname,
    //   planDuration: planduration,
    //   actualDuration: actualduration,
    //   tableData: tableData,
    // };

    //Retrieve existing tasks from local storage
    const existingTasks = getTaskData();

    //Add the new task to the existing tasks array
    const updateTasks = [...existingTasks, requestData];     

    //Store the updated tasks data in local storage
    storeTaskData(updateTasks);

    // Reset form fields
    // setProjectName("");
    // setPlanDuration("");
    // setActualDuration("");
    // setTableData([]);
  };

  return (                          //whatever we need to display that items are returend
    <div>
      <form className="m-5 px-4" onSubmit={handleSubmit}>     
        <div className="mb-3">
          <label htmlFor="exampleInputEmail1" className="form-label">
            Project Name
          </label>
          <input
            type="text"
            className="form-control"
            id="exampleInputEmail1"
            aria-describedby="emailHelp"
            onChange={(e) => setProjectName(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="exampleInputPassword1" className="form-label">
            Project Plan Duration
          </label>
          <input
            type="number"
            className="form-control"
            id="exampleInputPassword1"
            min="0"
            placeholder="Please enter the plan duration(in days)"
            onChange={(e) => setPlanDuration(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="exampleInputPassword1" className="form-label">
            Project Actual Duration
          </label>
          <input
            type="number"
            className="form-control"
            id="exampleInputPassword1"
            min="0"
            placeholder="Please enter the actual duration(in days)"
            onChange={(e) => setActualDuration(e.target.value)}
            required
          />
        </div>
        <Tableinput onUpdateTableData={setTableData} />
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </form>
      <div style={{ display: "flex", justifyContent: "center" }}>    
        <img
          src={imageContent}
          className="d-flex justify-content-center"
          alt="Red dot"
        />
      </div>

      <h4 className="text-center">Maximum End Time: {messageContent}</h4>
    </div>
  );
};

export default Taskform;