<?php
function logs($modulo,$texto){
        $hora = date("H:i:s"); // pega a hora
        $data = date("d-m-Y"); // pega o dia
        /*
            o "a+" abaixo significa:
            - Abre o arquivo para leitura e gravação; 
            - coloca o ponteiro no fim do arquivo. 
            - Se o arquivo não existir, tentar criá-lo.
        */
        $log = fopen("log/".$data.".txt", "a+");
        $escreve = fwrite($log, $modulo." - ".$hora." - ".$texto."\n");// Escreve
        fclose($log); // Fecha o arquivo
    }
    
function curl_get_contents($url)
{
  $ch = curl_init($url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
  curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
  curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
  $data = curl_exec($ch);
  curl_close($ch);
  return $data;
}

function deu_erro($tamanhoarquivo)
{
    $erro=FALSE;
    logs('Tamanho',strval($tamanhoarquivo));
    if($tamanhoarquivo==0 || $tamanhoarquivo==4411){
        $erro=TRUE;
        logs('Tamanho', 'Erro tamanho ='.strval($tamanhoarquivo));
    } else {
        logs('Tamanho', 'Ok tamanho ='.strval($tamanhoarquivo));
    }
    return $erro;
}

function baixar_arquivo($url,$arquivo){
    $file_name = basename($arquivo);
    $tempfilename=basename('temp'.$arquivo);
    logs('Baixar',$file_name);
    if (file_exists($file_name)) {
         logs('Baixar',$file_name.' pulei');
         return TRUE;
    }
    while($erro<5){
       if(file_put_contents( $tempfilename,curl_get_contents($url))){
          $tamanho=filesize($tempfilename);
          logs('Baixar', 'Tamanho='.$tamanho);
          if ($tamanho != 0 && $tamanho !=4411 && $tamanho != 150) {
              logs('Baixar',"Download com sucesso");
              rename($tempfilename, $file_name);
              return TRUE;
          } else {
            $erro=$erro+1;
            logs('Baixar',"Erro no download. Erro=".$erro);     
          }
        }
        else {
            $erro=$erro+1;
            logs('Baixar',"Erro no download. Erro=".$erro);   
        }
    }
    unlink($tempfilename);
    return FALSE;
}

?>