# Introduction #

This page details how to setup the smartgrid db for use with gridspice, what the tables & fields are, etc.

# Setting up the Database #

## Data import ##
If you have access to lidb.sql, you can import it into mysql with the following steps:

1. Start mysql with the following command at the shell
```
mysql -u root -p
```

2. Create a database for the data

```
create database lidb;
```

3. Exit mysql with

```
exit;
```

4. In the shell, import the database with the following command:

```
mysql -u root -p lidb < lidb.sql
```


---

Now all the smartmeter data is stored in a database called lidb.

## Creating a Database User ##
Now we will create a new user, lidb\_user, for the lidb database so that you don't have to access it from the root account every time

1. Start up mysql again

```
mysql -u root -p
```

2. Create the lidb\_user account

```
create user 'lidb_user' identified by 'PASSWORD';
```

Replace PASSWORD with whatever you'd like

3. grant privileges on lidb to the lidb\_user account

```
grant all privileges on lidb.* to lidb_user;
```

# Schema Information #
This section documents the schema of the tables in lidb

## Table: masterload\_all ##
This is a table of load intervals

Fields:

  * CUSTID - the customer id
  * DATE_- the date of the load intervals
  * QKWn - n is a number between 1 and 96.  so QWK1 contains the load for the first 15 minutes of the day, QWK2 contains the load for the next 15 minutes of the day, and so on. There is interval information for the whole day
  * PEAKUSE - TBD
  * OPEAKUSE - TBD
  * CELLID - TBD_

## Table: master\_tb3\_all ##
This is a table logging when a customer experienced a Demand Response event

Fields:

  * CPVSTART - Start time for the demand response event
  * CPVEND - End time for the demand response event
  * source - TBD
  * ACCT\_NM - TBD
  * custid - the id of the affected customer
  * date_- the date of the demand response event_

## Table: master\_tb5\_all ##
This table seems to describe information about a particular customer.

Fields:

  * CUSTID - the customer id
  * WEATHRID - the weather id (corresponds to table master\_tb8\_all)
  * OTHER FIELDS - TBD

## Table: master\_tb8\_all ##
This is a table of weather information for every day, keyed by WEATHRID

Fields:

  * WEATHRID - the weather id, a key that corresponds to WEATHRID in master\_tb5\_all
  * DATE