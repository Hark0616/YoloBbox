#PARA EL PROYECTO DE PERCEPCION
# Basics ROS 2 program to subscribe to real-time streaming 
# video from your built-in webcam
# Author:
# - Addison Sears-Collins
# - https://automaticaddison.com
  
# Import the necessary libraries
import rclpy # Python library for ROS 2
import serial #py serial para conectar con arduino
from std_msgs.msg import String
from std_msgs.msg import Int32
from rclpy.node import Node # Se importa todos los metodos de la clase NODE
from darknet_ros_msgs.msg._bounding_box import BoundingBox
from darknet_ros_msgs.msg._bounding_boxes import BoundingBoxes  #el tipo de mensaje para bounding box 

from sensor_msgs.msg import Image # se importa la clase IMAGE que implementa los mensajes tanto para publicar como para subscribirse a un topic
from cv_bridge import CvBridge # CvBridge el paquete que ayuda a convertir imagenes de ROS a OPenCV
import cv2 # libreria de openCV

 
class ImageSubscriber(Node):  #Creamos el nodo subscriptor/publicador imageSubscriber es subclase de la clase NODE

  def __init__(self):   # Creo el CONSTRUCTOR 
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('image_subscriber')   # 
      
    self.focal= 94.0
    self.Z= 70.0
    self.mot=0
    
    self.serialArduino= serial.Serial("/dev/ttyUSB0",9600) #defino el puerto y los baudios
    

    self.subscription = self.create_subscription(  #objeto que permite hacer subscripciones
      BoundingBoxes,     				     # le indico el tipo de mensaje
      '/darknet_ros/bounding_boxes', 				     # le indicamos el nombre del TOPIC pa subscribirse
      self.listener_callback, 		             # llamamos a callback
      10)					     # es el numero de mensajes que se van a guardar en la cola de subscripcion
    self.subscription # prevent unused variable warning
    
    
    self.publisher= self.create_publisher(   	     # objeto que permite hacer publicaciones
      Int32, 
      'BboxOut', 			     #el publicador crea el TOPIC si no existe
      10)

    # Used to convert between ROS and OpenCV images
   # self.br = CvBridge()
   
  def listener_callback(self, data):    # se define el callback: recibe mensaje data (sensor_msgs/image) lo procesa para tomar los bordes y publicarlo de regreso
    """
    Callback function.
    """
    # Display the message on the console
    #self.get_logger().info('Receiving video frame')
    
    
    
    self.mot=data.bounding_boxes[0].id  #1--roten   0--fresh
    print("Se envio el valor de {}.../n".format(self.mot))
    self.cad= str(self.mot)
    self.serialArduino.write(self.cad.encode('ascii'))
    
    print(self.mot)
    #encontramos X
    #data2= int(data)
    #X= (data.bounding_boxes*self.Z)/self.focal      #x=f*X/Z
    #self.publisher.publish(data)
    #Node.get_logger().info(X)
    #}rclpy.loginfo(X)
 
    #print (X)
 
    # Convert ROS Image message to OpenCV image
    #current_frame = self.br.imgmsg_to_cv2(data, "bgr8")  #se convierte el msgs a cv2 un arreglo de numpy con el cual ya se puede hacer mejoramiento
    
    # Hacemos pre procesamiento: primero escala de grises y luego extraccion de bordes
    #gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    #edges = cv2.Canny(gray,100,200)    
    
    # Mostramos la imagen en una ventana titulada Edges
    #cv2.imshow("Edges", edges)    
    #cv2.waitKey(3)
    
    # COnvertimos los bordes a un mensaje que ROS entienda para publicarlo de regreso
    #image_enhaced= self.br.cv2_to_imgmsg(edges, "mono8")
    #image_enhaced.header.frame_id= 'default_cam'   
        
    #es necesario que el topic que recibe los bordes, tenga el mismo frame_id 
    #publicamos los bordes en el topic creado:  /processed_image
    #out = Float64()
    #out.data = X
    #self.publisher.publish(out)
    
    
def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  image_subscriber = ImageSubscriber()   #llamamos al constructor de la clase
  
  
  # Spin the node so the callback function is called.
  rclpy.spin(image_subscriber)	#comienza a generar el objeto, hasta que alguien le de ctrl c y se destruye el nodo
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  image_subscriber.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()
