"use strict"


let searchForm = document.getElementById("searchForm");
let pageLinks = document.querySelectorAll(".page-link ");

if(searchForm){
pageLinks.forEach(function(link){
    link.addEventListener("click", function(e){
        e.preventDefault();
        let page = this.dataset.page;
        searchForm.innerHTML += `<input value=${page} name="page" value='hidden'>`;
        searchForm.submit();
    });
});
}

const tags = document.querySelectorAll(".project-tag");
tags.forEach(function(tag){
    tag.addEventListener("click", (e)=>{
        let tagId = e.target.dataset.tag;
        let projectId = e.target.dataset.project;

        fetch("http://127.0.0.1:8000/api/delete-tags/", {
            method: 'DELETE', headers: {
                'Content-Type' : 'application/json'
            },
            body: JSON.stringify({"project": projectId, 'tag': tagId})
        }).then(response => response.json()).then(data =>{
            e.target.remove();
        })
    });
})