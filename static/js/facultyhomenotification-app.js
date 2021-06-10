window.addEventListener('load',()=>{
    let ele = document.getElementsByClassName('reschedulebutton');

    for(let i=0;i<ele.length;i++){
        ele[i].addEventListener('click',()=>{
            ele[i].classList.add('processing');
            ele[i].textContent = 'Processing';
        })
    }
})