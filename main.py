#!/usr/bin/python

import urllib3
import requests
import string
import sys
import re
import certifi
import subprocess
import shlex
import logging
import os
import json
import httplib2

def add_upstream(this_host,upstream, upstream_status):
  '''
  Add server to upstream 
  '''
  data = {
       "server": this_host.hostname
  }

  x = 0
  found = 0
  while x < len(upstream_status):
    if this_host.hostname == upstream_status[x]['server']:
      found = 1 
    x = x + 1

  if found == 0:
    url = "http://127.0.0.1:8080/api/5/http/upstreams/{}/servers".format(upstream)
    #print "url: {}".format(url)
    r = requests.post(url=url, data=json.dumps(data))
    #print "{}".format(r.text)

def delete_upstream(this_host,upstream):
  #curl  -X POST -d '{ "server": "koba-report01.oradm.net" }' -s http://127.0.0.1:8080/api/5/http/results/beta_reporting/servers
  '''
  Remove a server from the upstream 
  '''

  #curl -GET  'http://127.0.0.1:8080/api/5/http/upstreams/beta_web' 
  url = "http://127.0.0.1:8080/api/5/http/upstreams/{}/servers".format(upstream)
  r = http.request('GET', url)
  results = json.loads(r.data)

  x = 0
  found = 0
  while x < len(results):
    if this_host.hostname == results[x]['server']:
      id = results[x]['id'] 
      found = 1 
    x = x + 1
    #print "{}".format(results['peers'][x])
    #id = results[x]['id']

  if found == 1:
    url = "http://127.0.0.1:8080/api/5/http/upstreams/{}/servers/{}".format(upstream,id)
    #print "{}".format(url)
    r = requests.delete(url)
    #print "{}".format(r.text)
    print "{} has been removed from the {} upstream".format(this_host.hostname,upstream)

def down_upstream(this_host,upstream,upstream_status):
  '''
  Up server in the pool
  '''

  header_content = {'Content-Type':'application/json'}

  x = 0
  while x < len(upstream_status):
    if this_host.hostname == upstream_status[x]['server']:
      id = upstream_status[x]['id']
    x = x + 1

  data = {
      "down": "true"
  }

  url = "http://127.0.0.1:8080/api/5/http/upstreams/{}/servers/{}".format(upstream,id)
  #print "{}".format(url)
  #print "{}".format(json.dumps(data))

  r = requests.patch(url, json.dumps(data), headers=header_content)
  get_status(this_host,upstream,upstream_status)


def drain_upstream(this_host,upstream,upstream_status):
  '''
  Up server in the pool
  '''
  # curl -X PATCH -d '{ "drain": true }' -s 'http://127.0.0.1:8080/api/5/http/upstreams/appservers/servers/0'    

  x = 0
  while x < len(upstream_status):
    if this_host.hostname == upstream_status[x]['server']:
      id = upstream_status[x]['id'] 
    x = x + 1

  data = {
      "drain": "true"
  }

  header_content = {'Content-Type':'application/json'}

  url = "http://127.0.0.1:8080/api/5/http/upstreams/{}/servers/{}".format(upstream,id)
  #print "{}".format(url)
  #print "return data: {}".format(json.dumps(data))

  r = requests.patch(url, json.dumps(data), headers=header_content)
  #print "{}".format(r.text)

def up_upstream(this_host,upstream,upstream_status):
  '''
  Up server in the pool
  '''
  data = {
      "down": "false"
  }
  
  header_content = {'Content-Type':'application/json'}

  x = 0
  while x < len(upstream_status):
    if this_host.hostname == upstream_status[x]['server']:
      id = upstream_status[x]['id']
    x = x + 1

  url = "http://127.0.0.1:8080/api/5/http/upstreams/{}/servers/{}".format(upstream,id)
  #print "{}".format(url)
  #print "{}".format(json.dumps(data))

  r = requests.patch(url, json.dumps(data), headers=header_content)

def print_status_host(this_host, upstream, upstream_status):
  '''
  print upstream info
  '''
  print "{}".format(upstream)

  x = 0
  while x < len(upstream_status):
    if this_host.hostname == upstream_status[x]['server']:
      print "server: {}   state: {}       id: {}".format(upstream_status[x]['server'],upstream_status[x]['state'],upstream_status[x]['id'])
    x = x + 1

def print_status(this_host, upstream, upstream_status):
  '''
  print upstream info
  '''
  print "{}".format(upstream)

  x = 0
  while x < len(upstream_status):
    print "server: {}	state: {}	id: {}".format(upstream_status[x]['server'],upstream_status[x]['state'],upstream_status[x]['id'])
    x = x + 1

 
def get_status(this_host, upstream, upstream_status):
  '''
  Get API status of pool
  '''
  #curl -GET  'http://127.0.0.1:8080/api/5/http/upstreams/beta_web' 
  url = "http://127.0.0.1:8080/api/5/http/upstreams/{}".format(upstream)
  r = http.request('GET', url)
  results = json.loads(r.data)

  #print "{}".format(r.data)

  x = 0
  while x < len(results['peers']):
    upstream_status.append({'server': results['peers'][x]['name'], 'state': results['peers'][x]['state'], 'id': results['peers'][x]['id']})
    x = x + 1
    #print "{}".format(results['peers'][x])
    #id = results[x]['id']


def main(this_host, http, action, upstream, upstream_status):
  '''
  Main Function 
  '''

  if action == "add":
    get_status(this_host, upstream, upstream_status)
    add_upstream(this_host,upstream, upstream_status)    
    get_status(this_host, upstream, upstream_status)
    print_status_host(this_host,upstream,upstream_status)
  elif action == "delete":
    get_status(this_host, upstream, upstream_status)
    delete_upstream(this_host,upstream)
  elif action == "down":
    get_status(this_host, upstream, upstream_status)
    down_upstream(this_host,upstream, upstream_status)
    upstream_status = []
    get_status(this_host,upstream,upstream_status)
    print_status_host(this_host, upstream, upstream_status)
  elif action == "drain":
    get_status(this_host, upstream, upstream_status)
    drain_upstream(this_host,upstream,upstream_status)
    upstream_status = []
    get_status(this_host,upstream,upstream_status)
    print_status_host(this_host, upstream, upstream_status)
  elif action == "up":
    get_status(this_host, upstream, upstream_status)
    up_upstream(this_host,upstream,upstream_status)
    upstream_status = []
    get_status(this_host,upstream,upstream_status)
    print_status_host(this_host, upstream, upstream_status)
  elif action == "status":
    get_status(this_host, upstream, upstream_status)
    print_status(this_host, upstream, upstream_status)

# Create urllib connection manager for requests
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

# Set up logger
log = logging.getLogger(__name__)

# Ignore Unverified HTTPS warning
urllib3.disable_warnings()

class host_name:
    # Initializer / Instance Attributes
    def __init__(self, hostname, ip):
      self.hostname = hostname
      self.ip = ip

    def description(self):
      return "{} has the ip {}".format(self.hostname,self.ip)


hostname = sys.argv[1]
ip = sys.argv[2]
action = sys.argv[3]
upstream = sys.argv[4]

this_host = host_name(hostname,ip)
#print "{}".format(this_host.description())

#build datastructure for upstream status
upstream_status = []
main(this_host,http,action,upstream,upstream_status)
