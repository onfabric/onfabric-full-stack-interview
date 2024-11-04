"use client";

import React, { useState } from "react";
import Keys from "./keys";
import Requests from "./requests";
import { ApiKey } from "@/types";

const Dashboard = ({ initialKeys }: { initialKeys: ApiKey[] }) => {
  const [selectedKey, setSelectedKey] = useState<ApiKey>(
    initialKeys[0]
  );
  return (
    <>
        <Keys
          selectedKey={selectedKey}
          setSelectedKey={setSelectedKey}
          initialKeys={initialKeys}
        />
        <Requests selectedKey={selectedKey} />

    </>
  );
};

export default Dashboard;
