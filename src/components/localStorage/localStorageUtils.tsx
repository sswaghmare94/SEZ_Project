// localStorageUtils.js

// Storing task data
export const storeTaskData = (tasks: any[]): void => {
  localStorage.setItem("tasks", JSON.stringify(tasks));
};

// Retrieving task data
export const getTaskData = () => {
  const storedTasks = localStorage.getItem("tasks");
  return storedTasks ? JSON.parse(storedTasks) : [];
};
