<?php
 
// Initialize a file URL to the variable
$url = 'http://compras.dados.gov.br/licitacoes/v1/licitacoes.json?item_material_classificacao=7010&data_publicacao_min=2022-03-01&data_publicacao_max=2022-03-31';


function get_page($url) {
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, True);
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl,CURLOPT_USERAGENT,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:7.0.1) Gecko/20100101 Firefox/7.0.1');
    $return = curl_exec($curl);
    curl_close($curl);
    return $return;
}

// true como segundo parametro do json_decode, signica que queremos os que vá buscar os conteudos como array em vez de ser como objeto, retire o true se quiser ir busca-los como objeto
////$contents = json_decode(get_page($url), true);
//print_r($contents);  // Array ( [status] => 1 [valores] => Array ( [USD] => Array ( [nome] => DÃ³lar [valor] => 3.5969 [ultima_consulta] => 1464713701 [fonte] => UOL Economia - http://economia.uol.com.br/ ) ) )


//$contents = get_page($url);
// Use basename() function to return the base name of file
$file_name = basename('licitacoes2022-03');
  
// Use file_get_contents() function to get the file
// from url and use file_put_contents() function to
// save the file by using base name
if(file_put_contents( $file_name,file_get_contents($url))) {
    echo "File downloaded successfully";
}
else {
    echo "File downloading failed.";
}


 
// Initialize the cURL session
$ch = curl_init($url);
 
// Initialize directory name where
// file will be save
$dir = './';
 
// Use basename() function to return
// the base name of file
$file_name = basename('licitacoes2022-02');
 
// Save file into file location
$save_file_loc = $dir . $file_name;
 
// Open file
$fp = fopen($save_file_loc, 'wb');
 
// It set an option for a cURL transfer
curl_setopt($ch, CURLOPT_FILE, $fp);
curl_setopt($ch, CURLOPT_HEADER, 0);
 
// Perform a cURL session
curl_exec($ch);
 
// Closes a cURL session and frees all resources
curl_close($ch);
 
// Close file
fclose($fp);


// Use basename() function to return the base name of file
//$file_name = basename('licitacoes2022-02get');
  
// Use file_get_contents() function to get the file
// from url and use file_put_contents() function to
// save the file by using base name
//if(file_put_contents( $file_name,file_get_contents($url))) {
//    echo "File downloaded successfully";
//}
//else {
//    echo "File downloading failed.";
//}
 
?>
