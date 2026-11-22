

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
