//compare part
var but_compare = document.getElementById("but_compare");

//course 1
const bscIT = () =>
{
    return bscit = {
    name: "Bachelor of Science in Software Engineering",
    level : "Graduate",
    duration : "4 years",
    el : "",
    fees: ,
    job : ""
    };
}

//course2
const bscCs = () =>
{
    return bsccs = {
    name: "Computer Science and Telecomunication Engineering",
    level : "Graduate",
    duration : "4 years",
    el : "",
    fees: ,
    job : ""
};
}

//course3
const ME = () =>
{
    return Me = {
    name: "Information comunication Engineering",
    level : "Gradute",
    duration : "4 years",
    el : "",
    fees :'',
    job : ""
};
}

//event
but_compare.addEventListener("click",()=>{
    var inp1 = document.getElementById("inp1").value;
    var inp2 = document.getElementById("inp2").value;
    let table_span = document.getElementById("table_span");

    let d1,d2;
    switch (inp1)
    {
        case "BScIT":
            d1 = bscIT();
            break;
        case "BScCS":
            d1 = bscCs();
            break;
        case "ME":
            d1 = ME();
    }
    switch (inp2)
    {
        case "BScIT":
            d2 = bscIT();
            break;
        case "BScCS":
            d2 = bscCs();
            break;
        case "ME":
            d2 = ME();
    }

    table_span.innerHTML = `
    <table  class="table table-bordered table-dark mt-3">
            <thead class="bg-primary">
              <tr style="color:white ; text-decoration: underline blue;">
                <th style=" width: 15%;" scope="col">Specfication</th>
                <th scope="col">${inp1}</th>
                <th scope="col">${inp2}</th>

              </tr>
            </thead>
            <tbody>
                <tr>
                    <th scope="row">Full form</th>
                    <td>${d1.name}</td>
                    <td>${d2.name}</td>

                  </tr>
              <tr>
                <th scope="row">course level</th>
                <td>${d1.level}</td>
                <td>${d2.level}</td>

              </tr>
              <tr>
                <th scope="row">duration</th>
                <td>${d1.duration}</td>
                <td>${d2.duration}</td>

              </tr>
              <tr>
                <th scope="row">eligibility</th>
                <td>${d1.el}</td>
                <td>${d2.el}</td>

              </tr>
              <tr>
                <th scope="row">course fees</th>
                <td>${d1.fees}, differ from various colleges </td>
                <td>${d2.fees}, differ from various colleges </td>

              </tr>
              <tr>
                <th scope="row">job position</th>
                <td>${d1.job}</td>
                <td>${d2.job}</td>

              </tr>
            </tbody>
          </table>`
})