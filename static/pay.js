


const btn1 = document.querySelector("#menubtn")
const menu1 = document.querySelector("#menus")

const btn2 = document.querySelector("#menubtn2")
const menu2 = document.querySelector("#menu")


btn1.addEventListener("click",(e)=>{
    e.stopPropagation()
    menu1.classList.toggle("hidden")
})


btn2.addEventListener("click",(e)=>{
    e.stopPropagation()
    menu2.classList.toggle("hidden")
})
menu1.addEventListener("click",(e)=>{
e.stopPropagation()
})
menu2.addEventListener("click",(e)=>{
  e.stopPropagation()
})

nav = document.querySelector("#nav")
btn3 = document.querySelector("#togglebtn")
label = document.querySelectorAll(".labels")

btn3.addEventListener("click",(e)=>{
  e.stopPropagation()
  nav.classList.toggle("w-[23%]")
  nav.classList.toggle("w-[8%]")
  label.forEach(el => {
    el.classList.toggle("hidden")
  });  
});


document.addEventListener("click",(e)=>{
        menu1.classList.add("show")
        menu2.classList.add("show")
        nav.classList.add("w-[23%]")
        label.forEach(el =>{
            el.classList.add("show")
        });
});

document.querySelectorAll('a[href="#"]').forEach(a=>{
a.addEventListener("click",(e)=>{
e.preventDefault()
})
});

const f = document.querySelector("#from_date")
const t = document.querySelector("#to_date")
const m = document.querySelector("#month")
const amt = document.querySelector("#amt")

// for tax
const tax_h = document.querySelector("#tax_t")
const tax_amt = document.querySelector("#pay_tax")

// save amt 
const save_h = document.querySelector("#save_h")
const save_amt = document.querySelector("#save_amt")
const actual_salary = document.querySelector("#salary_r")


function calc(){
  if (!f.value || !t.value ){
    return m.value =0
  }

  const [y1,m1,d1] = f.value.split("-").map(Number)
  const [y2,m2,d2] = t.value.split("-").map(Number)

  let months = (y2-y1)*12 + (m2-m1)


  annual_s = (amt.value) * 12
  if (annual_s < 1000000){
    tax_h.textContent = "Salary Tax : 1%"
    save_h.textContent ="Provident Fund (PF) : 5%"
    tax_amt.value = 1/100 * (months*amt.value)
    save_amt.value = 5/100 * (months*amt.value) 
    actual_salary.value = (months*amt.value)-(tax_amt.value)-(save_amt.value)

  }
  else{
    tax_h.textContent ="Salart Tax : 2%"
    save_h.textContent ="Provident Fund(PF) : 10%"
    tax_amt.value = 2/100 * (months*amt.value)
    save_amt.value = 10/100 * (months*amt.value) 
    actual_salary.value = (months*amt.value)-(tax_amt.value)-(save_amt.value)

  }

  if (d1>d2){
    months -= 1
  }
  m.value = months<0 ? 0 : months
}



f.addEventListener("change",()=>{
  t.min = f.value;
  calc()
})
t.addEventListener("change",calc)

