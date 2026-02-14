const hre = require("hardhat");

async function main() {

  const [deployer, validator2, validator3] = await hre.ethers.getSigners();

  const validators = [
    deployer.address,
    validator2.address,
    validator3.address
  ];

  const Registry = await hre.ethers.getContractFactory("ProductRegistry");

  const registry = await Registry.deploy(validators);

  await registry.waitForDeployment();

  console.log("ProductRegistry deployed to:", await registry.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
