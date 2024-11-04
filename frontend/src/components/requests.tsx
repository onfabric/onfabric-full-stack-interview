"use client";

import { ApiKey, UserRequest } from "@/types";
import React, { useEffect } from "react";
import { Table } from "./table";
import { getUserRequests } from "@/app/actions";

type Props = { selectedKey: ApiKey };

const Requests = (props: Props) => {
  const [isFetching, setIsFetching] = React.useState(false);
  const [requests, setRequests] =
    React.useState<UserRequest[]>([]);

  const fetchUserRequests = async () => {
    try {
      setIsFetching(true);
      const newRequests = await getUserRequests({
        keyId: props.selectedKey.id,
      });
      if (newRequests) setRequests(newRequests);
    } catch (e) {
      console.log(e);
    } finally {
      setIsFetching(false);
    }
  };

  useEffect(() => {

    fetchUserRequests();
  }, [props.selectedKey.id]);

  if (!props.selectedKey?.id) {
    return <>No Key Selected...</>;
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-row items-center justify-between">
        <div className="flex flex-row gap-2 items-center justify-start min-h-[40px]">
          <h2 className="font-semibold">
            Request History: <div className="inline font-thin italic">{props.selectedKey.name}</div>
          </h2>
          <div>{isFetching && "(loading...)"}</div>
        </div>
      </div>
      {requests && (
        <Table
          data={requests}
          columns={[
            {
              header: "ROUTE",
              accessor: "endpoint",
            },
            {
              header: "METHOD",
              accessor: "method",
            },
            {
              header: "STATUS",
              accessor: "status_code",
            },
            {
              header: "STATUS",
              accessor: "created_at",
            },
          ]}
        />
      )}
    </div>
  );
};

export default Requests;
