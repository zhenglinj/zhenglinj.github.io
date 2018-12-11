---
title: "初体验 Cloudera CDH"
excerpt: "介绍如何快速安装 Cloudera CDH"
category: "technology"
analytics: true
comments: true
tags: [hadoop, cloudera, cdh]
---
{% include JB/setup %}

<!-- TODO -->

---

## Cloudera Express

The Best Way to Get Started with Hadoop

Whether you are evaluating Hadoop to accelerate data processing, optimize the performance of your data warehouse, or perform new types of analysis on data sets that were previously out of reach, Cloudera Express is your key to successfully deploying Hadoop to solve your first use cases.

### Cloudera Express is installed via Cloudera Manager

Cloudera Manager is the recommended tool for installing Cloudera Express. It automatically downloads with Cloudera Express.

When installing Cloudera Express you will have the option to unlock Cloudera Enterprise features for a free 60-day trial.

Once the trial has concluded, the Cloudera Enterprise features will be disabled until you obtain and upload a license.

### Automated Installation

Ideal for trying Cloudera enterprise data hub, the installer will download Cloudera Manager from Cloudera's website and guide you through the setup process.

Pre-requisites: multiple, Internet-connected Linux machines, with SSH access, and significant free space in /var and /opt.

```
$ wget http://archive.cloudera.com/cm5/installer/latest/cloudera-manager-installer.bin
$ chmod u+x cloudera-manager-installer.bin
$ sudo ./cloudera-manager-installer.bin
```

### Production Installation

Users setting up Cloudera enterprise data hub for production use are encouraged to follow the installation instructions in our documentation. These instructions suggest explicitly provisioning the databases used by Cloudera Manager and walk through explicitly which packages need installation.
