async function getDataByYear() {
   try {
       const response = await fetch("/get-year", { method: "GET" });
       const data = await response.json();
       return data;
   }
   catch (error) {
       console.log(error);
   }
}

export {getDataByYear};
