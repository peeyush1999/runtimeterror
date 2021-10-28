function validateform(){  
    var name=document.myform.Name.value;  
    var password=document.myform.Password.value;  
    var x=document.myform.Email.value;  
    var atposition=x.indexOf("@");  
    var dotposition=x.lastIndexOf(".");   
    if (name==null || name==""){  
      alert("Name can't be blank");  
      return false;  
    }
    else if(password.length<6){  
      alert("Password must be at least 6 characters long.");  
      return false;  
    }
    else if(atposition<1 || dotposition<atposition+2 || dotposition+2>=x.length){  
        alert("Please enter a valid e-mail address \n atpostion:"+atposition+"\n dotposition:"+dotposition);  
        return false;  
    }  
   
   
} 
function validatesigninform() {
    var y=document.mysigninform.Email.value;  
    var atpositions=y.indexOf("@");  
    var dotpositions=y.lastIndexOf(".");  
    var spassword=document.mysigninform.Password.value;  
    
    if(atpositions<1 || dotpositions<atpositions+2 || dotpositions+2>=y.length){  
        alert("Please enter a valid e-mail address \n atpostion:"+atpositions+"\n dotposition:"+dotpositions);  
        return false;  
    }
    else if(spassword.length<6){  
        alert("sign inPassword must be at least 6 characters long.");  
        return false;  
    }    
    

}
