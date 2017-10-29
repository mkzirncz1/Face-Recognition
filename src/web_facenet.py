#importing libraries

import tensorflow as tf
import numpy as np
import web
import os
import time
import add_face
import facenet

#declare variables
model="trained_model/model.pb"
class_names=np.load('classnames.npy')
embeds=np.load('embed.npy')
labels=np.load('labels.npy')
image_dir='static/images/'

render = web.template.render('./templates/')
urls = ('/', 'index')
	
app = web.application(urls, globals())

#initialize tensorflow grpah
graph = tf.Graph()   
with graph.as_default():
      
        #start a tensorflow session
	sess_config = tf.ConfigProto()
        sess_config.gpu_options.per_process_gpu_memory_fraction = 0.90
        with tf.Session(config=sess_config) as sess:
            	
		# Load the model
                print('Loading feature extraction model')
            	facenet.load_model(model)
   		
		#define index class
		class index:
			def GET(self): 
				#display index.html template				
				return render.index(None,None,None)

    			def POST(self):
				#save user inputs
        			i = web.input()
				# if add face form submit
				if i.form_name == "add_face":
        				files = web.webapi.rawinput().get('file1')
        				face_name = i.new_face_name
				
					#save images in a list		
        				if not isinstance(files, list):
        			    		files = [files]
	
					#save faces to images directory
        				os.mkdir(image_dir+face_name)
        				for f in files:
        			    		target = image_dir+face_name
        			    		content = f.file.read()
        			    		with open(target +'/'+ f.filename,'w') as f:
        			        		f.write(content)
        	    	
    					#add face to database/numpy
					global class_names 
					global labels
					global embeds
					st = time.time()					
					updates=add_face.main(sess, graph, image_dir, class_names, labels, embeds)
 					class_names=updates[0]
					labels=updates[1]
					embeds=updates[2]
					
					faces=None
					find_image=None
					add_image=None
					
				
				return render.index(faces, add_image, find_image)

if __name__=='__main__':

	print('name again')
	app.run()
	
 		
