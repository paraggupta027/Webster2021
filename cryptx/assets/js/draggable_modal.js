
let modal_drag_area ;
let px,py;
let added = false;

$(document).ready(()=>{
    console.log("draggable_js_start")
    modal_drag_area =document.getElementsByClassName('modal-drag-area')[0];
    modal = document.getElementsByClassName('draggable-modal')[0];
    
    modal_drag_area.addEventListener('mousedown',addMouseDrag)
    window.addEventListener('mouseup',removeMouseDrag)
     offsety = modal.getBoundingClientRect().top;
     offsetx = modal.getBoundingClientRect().left;
    console.log("draggable_js_end")
}
);
function addMouseDrag(){
    console.log('Mouse down')
    if(!added){
    modal.addEventListener('mousemove',dragModal)
    added=true;
    modal.user_select = false;
}

}
function removeMouseDrag(){
    if(added){
    console.log(' mouse up')
    modal.removeEventListener('mousemove',dragModal)
    added=false;

}
}
function dragModal(e){

    mousey = e.movementY;
    mousex = e.movementX;
    console.log(modal.style.left,    offsetx
,mousex        )
    // calcx = offsetx + mousex/
    
    offsetx+= mousex;
    offsety+= mousey;
    modal.style.left =offsetx +"px";
    modal.style.top = offsety +"px";
    // modal.style.user-select = 
}