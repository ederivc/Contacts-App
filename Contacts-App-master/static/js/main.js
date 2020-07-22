const bdelete = document.querySelectorAll(".btn-delete")

if(bdelete){
    const myArray = Array.from(bdelete);
    myArray.forEach((btn) =>{
        btn.addEventListener("click", (e) => {
            if(!confirm("The user will be deleted")){
                e.preventDefault();
            }
        });
    });
}

function filesize(file){
    document.cookie = `filesize=${file.files[0].size}`;
}
