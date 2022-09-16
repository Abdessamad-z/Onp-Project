function changeDate(value) {
    value.state = true
    const ele = value.parentElement.parentElement.querySelectorAll("td")[2];
    if (ele.innerText.search("(modifié)") === -1)
        if (ele.innerText.search("(supprimé)") === -1)
            ele.innerText += " (modifié)"
        else{
            let index=ele.innerText.search("(supprimé)")
            ele.innerText=ele.innerText.slice(0,index-2)+" (modifié)"+ele.innerText.slice(index-2)
            }
}

function myRemoveRow(value) {
    const ele = value.parentElement.parentElement.querySelectorAll("td")[2];
    const check = value.parentElement.parentElement.querySelectorAll("td")[4];
    if (value.checked)
        ele.innerText += " (supprimé)"
    else
        ele.innerText = ele.innerText.replace("(supprimé)", "")
}