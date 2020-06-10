
EXAMPLE:

<html>
   <head>
      <meta charset="UTF-8" />
      <link rel="stylesheet" type="text/css" href="css/style.css">
   </head>
   <?php
      if (isset($_POST['LightON'])) {
          exec("python /home/pi/lightOn.py");
      }
      if (isset($_POST['LightOFF'])) {
          exec("python /home/pi/lightOff.py");
      }
   ?>
   <form method="post">
      <button class="btn" name="LightON">Light ON</button>&nbsp;
      <button class="btn" name="LightOFF">Light OFF</button><br><br>
   </form>
</html>

