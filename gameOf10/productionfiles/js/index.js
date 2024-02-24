function show_hide_login_view(){
    const rule_view = document.querySelector('#login-container');

    if (rule_view.style.display == 'flex'){
        rule_view.style.display = 'none';
    }else{
        rule_view.style.display = 'flex';
    }
}

document.querySelector('#login-container').addEventListener('click',event => {
    if (event.target == document.querySelector('#login-container')){
        show_hide_login_view()
    }
})