<!--
LOAD THE XML FILE ON THE SERVER
XML="queryoptions.xml"
CODE FROM W3SCHOOLS
-->
<script>
  if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
    }
  else
      {// code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
  xmlhttp.open("GET","{{ STATIC_URL }}/site_media/static/queryoptions.xml",false);
  xmlhttp.send();
  xmlDoc=xmlhttp.responseXML; 
</script>

<!--
VALIDATE FORM
-->
<script>
function validateForm(){
	var formobj = document.forms[0];
	var counter = 0;
	var db_counter = 0;
	
	for (var j = 0; j < formobj.elements.length; j++)
	{
		if (formobj.elements[j].type == "checkbox" && formobj.elements[j].name == "databases")
		{
			if (formobj.elements[j].checked)
			{
				db_counter++;
			}	
		}  
		
		if (formobj.elements[j].type == "checkbox" && formobj.elements[j].name != "zipped" && formobj.elements[j].name != "databases")
		{
			if (formobj.elements[j].checked)
			{
				counter++;
			}	
		}       
	}
	
	if (db_counter < 1){
		alert ("Include a Gene/Protein Consequence");
		return false;
	}
	
	if (counter < 1){
		alert ("Select a feature to map");
		return false;
	}
	else {
		$('#loading').show();
		return true;
	}
}
</script>