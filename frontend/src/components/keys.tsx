"use client";

import React, { Dispatch, SetStateAction, useEffect, useState } from "react";
import { Table } from "./table";
import { ApiKey } from "@/types";
import { createApiKey, getApiKeys } from "@/app/actions";

type Props = {
  initialKeys: ApiKey[];
  setSelectedKey: Dispatch<SetStateAction<ApiKey>>;
  selectedKey: ApiKey;
};

const Keys = (props: Props) => {
  const [keys, setKeys] = React.useState(props.initialKeys);
  const [keyName, setKeyName] = React.useState("");
  const [isFetching, setIsFetching] = React.useState(false);

  const fetchKeys = async () => {
    try {
      setIsFetching(true);
      const newKeys = await getApiKeys();
      if (newKeys) setKeys(newKeys);
    } catch (e) {
      console.log(e);
    } finally {
      setIsFetching(false);
    }
  };

  const handleAddKey = async () => {
    try {
      const newKey = await createApiKey({ name: keyName });
      if (newKey === null) {
        throw Error("Failed to create api key");
      }
      fetchKeys();
      setKeyName("");
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchKeys();
  }, []);

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center gap-2">
        <div className="flex flex-row gap-2 items-center justify-start min-h-[40px]">
          <h2 className="font-semibold">Active Keys</h2>
          <div>{isFetching && "(loading...)"}</div>
        </div>
        <div className="flex flex-row gap-2">
          <input
            type="text"
            value={keyName}
            onChange={(e) => setKeyName(e.target.value)}
            placeholder="Enter key name"
            className="px-4 py-2 text-sm border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            disabled={!keyName}
            style={
              keyName ? {} : { backgroundColor: "gray", cursor: "not-allowed" }
            }
            onClick={handleAddKey}
            className="cursor-pointer px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
          >
            Add New Key
          </button>
        </div>
      </div>

      <Table
        data={keys}
        columns={[
          {
            header: "",
            accessor: "id",
            render: (value, item) => {
              return (
                <input
                  id="default-checkbox"
                  type="checkbox"
                  checked={value === props.selectedKey.id}
                  onChange={() => props.setSelectedKey(item)}
                  className="cursor-pointer w-3 h-3
                   text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                />
              );
            },
          },
          {
            header: "Name",
            accessor: "name",
          },
          {
            header: "Key",
            accessor: "key",
            render: (value: string | undefined) => {
              return (
                <span className="font-mono bg-gray-50 px-2 py-1 rounded-md text-xs">
                  {value}
                </span>
              );
            },
          },
          {
            header: "Last Used",
            accessor: "last_used_at",
            render: (value: string | undefined) =>
              value ? new Date(value).toLocaleString() : "Never",
          },
          {
            header: "Created",
            accessor: "created_at",
            render: (value: string | undefined) =>
              value ? new Date(value).toLocaleString() : "-",
          },
        ]}
      />
    </div>
  );
};

export default Keys;
