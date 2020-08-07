var page = window.location
page = String(page).split("/")
if (page[page.length-1] == "")   {
    document.getElementsByClassName('nav-home')[0].classList.add("active")

}
if (page[page.length-1] == "toDoList")   {
    document.getElementsByClassName('nav-toDo')[0].classList.add("active")

}
if (page[page.length-1] == "register")   {
    document.getElementsByClassName('nav-signUp')[0].classList.add("active")

}
if (page[page.length-1] == "login")   {
    document.getElementsByClassName('nav-signIn')[0].classList.add("active")

}
if (page[page.length-1] == "profile")   {
    document.getElementsByClassName('nav-profile')[0].classList.add("active")

}