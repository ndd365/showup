FROM node:argon
  
# Create the code directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./express/showup/package.json /usr/src/app/package.json
RUN npm install

# Copy the source into the image
COPY ./express/showup/app.js /usr/src/app/
COPY ./express/showup/public /usr/src/app/public
COPY ./express/showup/views /usr/src/app/views
COPY ./express/showup/bin /usr/src/app/bin
COPY ./express/showup/package.json /usr/src/app/
COPY ./express/showup/routes /usr/src/app/routes
  
# for local debugging using source maps we will serve the original source files at a special location
RUN mkdir -p /usr/src/app/debug/javascripts
COPY ./frontend/src /usr/src/app/debug/javascripts
  
# Uglify the js
WORKDIR /usr/src/app/debug/javascripts
RUN npm install uglify-js -g
RUN mkdir -p /usr/src/app/public/javascripts
  
# RUN uglifyjs <all src files to uglify using path relative to working dir> --output ../../public/javascripts/showup.min.js --source-map showup.min.js.map --source-map-root http://localhost:3000/debug/javascripts/ --source-map-url http://localhost:3000/debug/javascripts/showup.min.js.map -m -r 'angular,$,require,exports'
  
WORKDIR /usr/src/app
  
EXPOSE 3000
CMD [ "npm", "start" ]
# CMD [ "nodemon", "server.js", "--ignore", "backup_data/"]