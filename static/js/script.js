function updateDateTime()
    {
      var split = new Date().toString().split(" ");
      dateTime=split[1]+" "+split[2]+", "+split[3] + " "+split[4]+" "+split[6]+" "+split[7]+" "+split[8]

      document.getElementById('time').innerText = dateTime;
      
    }

    setInterval(function(){ updateDateTime(); }, 1000);
